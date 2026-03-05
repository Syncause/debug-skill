#!/usr/bin/env python3
"""Fail-closed workflow gate runner driven by a skill-local JSON contract.

The contract can be loaded from:
1) A `--spec` JSON file, or
2) A fenced block in SKILL.md:
   ```gate-spec-json
   { ... }
   ```
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, NoReturn, Tuple


SPEC_FENCE_PATTERN = re.compile(
    r"```gate-spec-json\s*\n(?P<body>.*?)\n```", re.DOTALL | re.MULTILINE
)
DEFAULT_TIMEOUT_SEC = 300


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def fail(msg: str, code: int = 2) -> NoReturn:
    eprint(f"ERROR: {msg}")
    raise SystemExit(code)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"File not found: {path}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path}: {exc}")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def spec_hash(spec: Dict[str, Any]) -> str:
    body = json.dumps(spec, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def deep_merge(base: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in incoming.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def get_json_path(data: Any, dotted_path: str) -> Tuple[bool, Any]:
    current = data
    if not dotted_path:
        return True, current
    for token in dotted_path.split("."):
        if isinstance(current, dict) and token in current:
            current = current[token]
            continue
        if isinstance(current, list):
            try:
                index = int(token)
            except ValueError:
                return False, None
            if index < 0 or index >= len(current):
                return False, None
            current = current[index]
            continue
        return False, None
    return True, current


def render_templates(value: Any, context: Dict[str, str]) -> Any:
    if isinstance(value, str):
        out = value
        for key, replacement in context.items():
            out = out.replace(f"${{{key}}}", replacement)
        return out
    if isinstance(value, dict):
        return {k: render_templates(v, context) for k, v in value.items()}
    if isinstance(value, list):
        return [render_templates(v, context) for v in value]
    return value


def resolve_path(path_value: str, cwd: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (cwd / path).resolve()


def get_git_changed_files(cwd: Path) -> List[str]:
    proc = subprocess.run(
        ["git", "-C", str(cwd), "status", "--porcelain"],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    changed: List[str] = []
    for line in proc.stdout.splitlines():
        if not line:
            continue
        entry = line[3:]
        if " -> " in entry:
            entry = entry.split(" -> ", 1)[1]
        changed.append(entry.strip())
    return sorted(set(changed))


def load_spec(skill_path: Path | None, spec_path: Path | None) -> Dict[str, Any]:
    if spec_path:
        spec = load_json(spec_path)
    else:
        if skill_path is None:
            fail("Provide either --spec or --skill.")
        skill_text = read_text(skill_path)
        match = SPEC_FENCE_PATTERN.search(skill_text)
        if not match:
            fail(
                "No `gate-spec-json` fenced block found in SKILL.md. "
                "Provide --spec or embed a contract."
            )
        try:
            spec = json.loads(match.group("body"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid embedded gate spec JSON in {skill_path}: {exc}")
    validate_spec(spec)
    return spec


def validate_spec(spec: Dict[str, Any]) -> None:
    if not isinstance(spec, dict):
        fail("Gate spec must be a JSON object.")
    if not isinstance(spec.get("steps"), list) or not spec["steps"]:
        fail("Gate spec must include a non-empty `steps` array.")
    seen = set()
    for index, step in enumerate(spec["steps"], start=1):
        if not isinstance(step, dict):
            fail(f"Step #{index} must be an object.")
        step_id = step.get("id")
        if not step_id or not isinstance(step_id, str):
            fail(f"Step #{index} is missing string `id`.")
        if step_id in seen:
            fail(f"Duplicate step id in gate spec: {step_id}")
        seen.add(step_id)
        if "verifiers" in step and not isinstance(step["verifiers"], list):
            fail(f"Step `{step_id}`: `verifiers` must be an array.")
        if "operations" in step and not isinstance(step["operations"], list):
            fail(f"Step `{step_id}`: `operations` must be an array.")
        if "gates" in step:
            if not isinstance(step["gates"], list) or not step["gates"]:
                fail(f"Step `{step_id}`: `gates` must be a non-empty array.")
            gate_ids = set()
            for gate in step["gates"]:
                if not isinstance(gate, dict):
                    fail(f"Step `{step_id}`: each gate must be an object.")
                gate_id = gate.get("id")
                if not gate_id or not isinstance(gate_id, str):
                    fail(f"Step `{step_id}`: each gate must have string `id`.")
                if gate_id in gate_ids:
                    fail(f"Step `{step_id}`: duplicate gate id `{gate_id}`.")
                gate_ids.add(gate_id)
                mode = gate.get("mode", "hard")
                if mode not in {"hard", "soft"}:
                    fail(
                        f"Step `{step_id}` gate `{gate_id}`: mode must be `hard` or `soft`."
                    )
                if "verifiers" not in gate:
                    fail(
                        f"Step `{step_id}` gate `{gate_id}`: missing `verifiers` array."
                    )
                if not isinstance(gate["verifiers"], list):
                    fail(
                        f"Step `{step_id}` gate `{gate_id}`: `verifiers` must be an array."
                    )


def normalize_step_gates(step: Dict[str, Any]) -> List[Dict[str, Any]]:
    gates = step.get("gates")
    if gates:
        return gates
    # Backward-compatible fallback: treat flat verifiers as one hard gate.
    return [
        {
            "id": "default",
            "mode": "hard",
            "verifiers": step.get("verifiers", []),
        }
    ]


def ensure_state(
    state_path: Path,
    spec: Dict[str, Any],
    skill_path: Path | None,
    cwd: Path,
) -> Dict[str, Any]:
    workflow = spec.get("workflow", "workflow")
    if state_path.exists():
        state = load_json(state_path)
    else:
        baseline_changes = get_git_changed_files(cwd)
        state = {
            "workflow": workflow,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "skill_path": str(skill_path) if skill_path else None,
            "cwd": str(cwd),
            "spec_hash": spec_hash(spec),
            "baseline_changed_files": baseline_changes,
            "steps": {},
        }
        write_json(state_path, state)
    new_hash = spec_hash(spec)
    if state.get("spec_hash") != new_hash:
        state["spec_hash"] = new_hash
        state["updated_at"] = now_iso()
    state.setdefault("steps", {})
    state.setdefault("baseline_changed_files", get_git_changed_files(cwd))
    return state


def select_steps(
    spec: Dict[str, Any],
    step: str | None,
    from_step: str | None,
    to_step: str | None,
) -> List[Dict[str, Any]]:
    steps = spec["steps"]
    ids = [s["id"] for s in steps]
    if step:
        if step not in ids:
            fail(f"Unknown step id: {step}")
        return [next(s for s in steps if s["id"] == step)]
    if from_step and from_step not in ids:
        fail(f"Unknown --from-step id: {from_step}")
    if to_step and to_step not in ids:
        fail(f"Unknown --to-step id: {to_step}")
    start = ids.index(from_step) if from_step else 0
    end = ids.index(to_step) if to_step else len(steps) - 1
    if end < start:
        fail("--to-step must not come before --from-step.")
    return steps[start : end + 1]


def run_shell_command(
    cmd: str,
    cwd: Path,
    timeout_sec: int,
    env: Dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update({k: str(v) for k, v in env.items()})
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        shell=True,
        text=True,
        capture_output=True,
        timeout=timeout_sec,
        env=merged_env,
        check=False,
    )


def verifier_result(
    verifier_id: str,
    ok: bool,
    message: str,
    details: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    result = {
        "id": verifier_id,
        "ok": ok,
        "message": message,
        "checked_at": now_iso(),
    }
    if details:
        result["details"] = details
    return result


def verify_git_no_new_changes(
    state: Dict[str, Any],
    cwd: Path,
    allowed_new_changes: List[str] | None = None,
) -> Tuple[bool, str, Dict[str, Any]]:
    baseline = set(state.get("baseline_changed_files", []))
    current = set(get_git_changed_files(cwd))
    new_changes = sorted(current - baseline)
    if allowed_new_changes:
        filtered = []
        for path in new_changes:
            if any(Path(path).match(pattern) for pattern in allowed_new_changes):
                continue
            filtered.append(path)
        new_changes = filtered
    if new_changes:
        return (
            False,
            "Detected new git changes outside the baseline.",
            {"new_changes": new_changes},
        )
    return True, "No new git changes relative to baseline.", {}


def evaluate_verifier(
    verifier: Dict[str, Any],
    step_state: Dict[str, Any],
    state: Dict[str, Any],
    cwd: Path,
    context: Dict[str, str],
) -> Dict[str, Any]:
    verifier = render_templates(verifier, context)
    verifier_id = verifier.get("id", verifier.get("type", "verifier"))
    verifier_type = verifier.get("type")
    if not verifier_type:
        return verifier_result(verifier_id, False, "Missing verifier `type`.")

    if verifier_type == "shell":
        cmd = verifier.get("cmd")
        if not cmd:
            return verifier_result(verifier_id, False, "Missing shell verifier `cmd`.")
        timeout_sec = int(verifier.get("timeout_sec", DEFAULT_TIMEOUT_SEC))
        expected_exit = int(verifier.get("exit_code", 0))
        proc = run_shell_command(cmd, cwd=cwd, timeout_sec=timeout_sec)
        combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
        contains = verifier.get("contains")
        not_contains = verifier.get("not_contains")
        ok = proc.returncode == expected_exit
        if contains is not None and contains not in combined:
            ok = False
        if not_contains is not None and not_contains in combined:
            ok = False
        message = (
            f"shell exit={proc.returncode}, expected={expected_exit}"
            if ok
            else f"shell verifier failed (exit={proc.returncode}, expected={expected_exit})"
        )
        return verifier_result(
            verifier_id,
            ok,
            message,
            {"stdout": proc.stdout[-1000:], "stderr": proc.stderr[-1000:]},
        )

    if verifier_type in {"file_exists", "file_not_exists", "file_contains", "file_not_contains"}:
        path_value = verifier.get("file") or verifier.get("path")
        if not path_value:
            return verifier_result(verifier_id, False, "Missing `file` for file verifier.")
        path = resolve_path(str(path_value), cwd)
        if verifier_type == "file_exists":
            ok = path.exists()
            return verifier_result(verifier_id, ok, f"{path} exists={ok}")
        if verifier_type == "file_not_exists":
            ok = not path.exists()
            return verifier_result(verifier_id, ok, f"{path} exists={not ok}")
        if not path.exists():
            return verifier_result(verifier_id, False, f"File does not exist: {path}")
        content = read_text(path)
        needle = verifier.get("pattern")
        if needle is None:
            return verifier_result(verifier_id, False, "Missing `pattern` for content verifier.")
        if verifier_type == "file_contains":
            ok = needle in content
            return verifier_result(verifier_id, ok, f"pattern found={ok} in {path}")
        ok = needle not in content
        return verifier_result(verifier_id, ok, f"pattern absent={ok} in {path}")

    if verifier_type in {"json_path_exists", "json_path_equals"}:
        path_value = verifier.get("file")
        dotted = verifier.get("path")
        if not path_value or dotted is None:
            return verifier_result(
                verifier_id, False, "Missing `file` or `path` for JSON verifier."
            )
        target = resolve_path(str(path_value), cwd)
        if not target.exists():
            return verifier_result(verifier_id, False, f"JSON file not found: {target}")
        data = load_json(target)
        exists, value = get_json_path(data, str(dotted))
        if verifier_type == "json_path_exists":
            return verifier_result(verifier_id, exists, f"path exists={exists}: {dotted}")
        expected = verifier.get("value")
        ok = exists and value == expected
        return verifier_result(
            verifier_id,
            ok,
            f"path equals expected={ok}: {dotted}",
            {"actual": value, "expected": expected},
        )

    checkpoints = step_state.setdefault("checkpoints", {})
    if verifier_type == "checkpoint_path_exists":
        dotted = verifier.get("path", "")
        exists, _ = get_json_path(checkpoints, str(dotted))
        return verifier_result(verifier_id, exists, f"checkpoint path exists={exists}: {dotted}")

    if verifier_type == "checkpoint_path_equals":
        dotted = verifier.get("path", "")
        exists, value = get_json_path(checkpoints, str(dotted))
        expected = verifier.get("value")
        ok = exists and value == expected
        return verifier_result(
            verifier_id,
            ok,
            f"checkpoint path equals expected={ok}: {dotted}",
            {"actual": value, "expected": expected},
        )

    if verifier_type == "checkpoint_array_nonempty":
        dotted = verifier.get("path", "")
        exists, value = get_json_path(checkpoints, str(dotted))
        ok = exists and isinstance(value, list) and len(value) > 0
        return verifier_result(
            verifier_id, ok, f"checkpoint array non-empty={ok}: {dotted}"
        )

    if verifier_type == "git_no_new_changes":
        allowed = verifier.get("allowed_new_changes", [])
        ok, message, details = verify_git_no_new_changes(state, cwd, allowed)
        return verifier_result(verifier_id, ok, message, details)

    return verifier_result(verifier_id, False, f"Unsupported verifier type: {verifier_type}")


def run_step(
    step: Dict[str, Any],
    state: Dict[str, Any],
    cwd: Path,
    artifacts_root: Path,
    verify_only: bool,
    fail_closed: bool,
    context_base: Dict[str, str],
) -> Tuple[bool, Dict[str, Any]]:
    step_id = step["id"]
    step_state = state["steps"].setdefault(step_id, {})
    step_state["title"] = step.get("title")
    step_state["updated_at"] = now_iso()
    step_state["status"] = "running"
    step_state["operations"] = []
    step_state["gates"] = []
    step_state["verifiers"] = []
    step_state["warnings"] = []
    step_state["failure_reason"] = None
    step_context = dict(context_base)
    step_context["STEP_ID"] = step_id

    for dependency in step.get("requires", []):
        dep_status = state["steps"].get(dependency, {}).get("status")
        if dep_status != "passed":
            reason = f"dependency `{dependency}` is not passed (status={dep_status})"
            step_state["status"] = "blocked"
            step_state["failure_reason"] = reason
            return False, step_state

    if not verify_only:
        for index, operation in enumerate(step.get("operations", []), start=1):
            operation = render_templates(operation, step_context)
            op_id = operation.get("id", f"op-{index}")
            op_type = operation.get("type", "manual")
            record: Dict[str, Any] = {
                "id": op_id,
                "type": op_type,
                "run_at": now_iso(),
            }
            if op_type == "manual":
                record["status"] = "manual"
                record["message"] = operation.get("description", "Manual step.")
                step_state["operations"].append(record)
                continue
            if op_type != "shell":
                record["status"] = "failed"
                record["message"] = f"Unsupported operation type: {op_type}"
                step_state["operations"].append(record)
                step_state["status"] = "failed"
                step_state["failure_reason"] = record["message"]
                return False, step_state
            cmd = operation.get("cmd")
            if not cmd:
                record["status"] = "failed"
                record["message"] = "Missing shell operation `cmd`."
                step_state["operations"].append(record)
                step_state["status"] = "failed"
                step_state["failure_reason"] = record["message"]
                return False, step_state
            timeout_sec = int(operation.get("timeout_sec", DEFAULT_TIMEOUT_SEC))
            expected_exit = int(operation.get("exit_code", 0))
            proc = run_shell_command(
                cmd,
                cwd=resolve_path(operation.get("cwd", "."), cwd),
                timeout_sec=timeout_sec,
                env=operation.get("env"),
            )
            step_artifacts = artifacts_root / step_id
            step_artifacts.mkdir(parents=True, exist_ok=True)
            stdout_file = step_artifacts / f"{op_id}.stdout.log"
            stderr_file = step_artifacts / f"{op_id}.stderr.log"
            stdout_file.write_text(proc.stdout or "", encoding="utf-8")
            stderr_file.write_text(proc.stderr or "", encoding="utf-8")
            record.update(
                {
                    "status": "passed" if proc.returncode == expected_exit else "failed",
                    "exit_code": proc.returncode,
                    "expected_exit_code": expected_exit,
                    "stdout_file": str(stdout_file),
                    "stderr_file": str(stderr_file),
                    "cmd": cmd,
                }
            )
            step_state["operations"].append(record)
            if record["status"] != "passed":
                step_state["status"] = "failed"
                step_state["failure_reason"] = (
                    f"operation `{op_id}` failed with exit={proc.returncode}"
                )
                if fail_closed:
                    return False, step_state

    hard_gate_failures = 0
    soft_gate_failures = 0
    for gate in normalize_step_gates(step):
        gate_id = gate.get("id", "gate")
        mode = gate.get("mode", "hard")
        gate_record = {
            "id": gate_id,
            "mode": mode,
            "checked_at": now_iso(),
            "verifiers": [],
            "failed_verifiers": 0,
            "passed_verifiers": 0,
            "ok": True,
        }
        for index, verifier in enumerate(gate.get("verifiers", []), start=1):
            verifier = dict(verifier)
            verifier.setdefault("id", f"{gate_id}-verifier-{index}")
            result = evaluate_verifier(verifier, step_state, state, cwd, step_context)
            gate_record["verifiers"].append(result)
            step_state["verifiers"].append(result)
            if result["ok"]:
                gate_record["passed_verifiers"] += 1
            else:
                gate_record["failed_verifiers"] += 1
                gate_record["ok"] = False
        step_state["gates"].append(gate_record)
        if gate_record["failed_verifiers"] > 0:
            if mode == "hard":
                hard_gate_failures += 1
            else:
                soft_gate_failures += 1

    if soft_gate_failures:
        step_state["warnings"].append(
            f"{soft_gate_failures} soft gate(s) failed for step `{step_id}`."
        )

    if step_state.get("status") == "failed" and fail_closed:
        return False, step_state
    if hard_gate_failures:
        step_state["status"] = "failed"
        step_state["failure_reason"] = (
            f"{hard_gate_failures} hard gate(s) failed for step `{step_id}`."
        )
        return False, step_state
    if step_state.get("status") != "failed":
        step_state["status"] = "passed"
        step_state["failure_reason"] = None
    return True, step_state


def print_status(spec: Dict[str, Any], state: Dict[str, Any]) -> None:
    print(f"Workflow: {spec.get('workflow', 'workflow')}")
    print(f"State file: {state.get('_state_path')}")
    print(f"Updated: {state.get('updated_at')}")
    for step in spec["steps"]:
        step_id = step["id"]
        step_state = state.get("steps", {}).get(step_id, {})
        status = step_state.get("status", "pending")
        reason = step_state.get("failure_reason")
        if reason:
            print(f"- {step_id}: {status} ({reason})")
        else:
            print(f"- {step_id}: {status}")
        for warning in step_state.get("warnings", []):
            print(f"  warning: {warning}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail-closed gate runner for SKILL workflows."
    )
    parser.add_argument("--skill", help="Path to SKILL.md")
    parser.add_argument("--spec", help="Path to JSON gate spec (optional)")
    parser.add_argument("--state", help="Path to state file (optional)")
    parser.add_argument(
        "--cwd",
        default=".",
        help="Workspace root for command execution and relative paths (default: current directory).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize state and baseline.")

    run_parser = subparsers.add_parser("run", help="Run operations and verifiers.")
    run_parser.add_argument("--step", help="Run only a single step id.")
    run_parser.add_argument("--from-step", help="Start from this step id.")
    run_parser.add_argument("--to-step", help="Stop at this step id.")
    run_parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Skip operations and execute verifiers only.",
    )

    verify_parser = subparsers.add_parser("verify", help="Run verifiers only.")
    verify_parser.add_argument("--step", help="Verify only a single step id.")
    verify_parser.add_argument("--from-step", help="Start from this step id.")
    verify_parser.add_argument("--to-step", help="Stop at this step id.")

    checkpoint_parser = subparsers.add_parser(
        "checkpoint",
        help="Merge JSON evidence into a step checkpoint.",
    )
    checkpoint_parser.add_argument("--step", required=True, help="Step id to update.")
    checkpoint_group = checkpoint_parser.add_mutually_exclusive_group(required=True)
    checkpoint_group.add_argument("--json", help="Inline JSON object to merge.")
    checkpoint_group.add_argument("--json-file", help="Path to JSON object file.")

    subparsers.add_parser("status", help="Show workflow step statuses.")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cwd = Path(args.cwd).resolve()
    skill_path = Path(args.skill).resolve() if args.skill else None
    spec_path = Path(args.spec).resolve() if args.spec else None
    spec = load_spec(skill_path, spec_path)
    workflow_name = spec.get("workflow", "workflow")
    default_state = cwd / ".gate" / workflow_name / "state.json"
    state_path = Path(args.state).resolve() if args.state else default_state
    artifacts_root = state_path.parent / "artifacts"
    fail_closed = bool(spec.get("fail_closed", True))
    state = ensure_state(state_path, spec, skill_path, cwd)
    state["_state_path"] = str(state_path)
    context = {
        "CWD": str(cwd),
        "SKILL_DIR": str(skill_path.parent) if skill_path else "",
    }

    if args.command == "init":
        state["updated_at"] = now_iso()
        write_json(state_path, {k: v for k, v in state.items() if k != "_state_path"})
        print(f"Initialized gate state: {state_path}")
        print(f"Baseline changed files: {len(state.get('baseline_changed_files', []))}")
        return 0

    if args.command == "checkpoint":
        step_id = args.step
        known_ids = {step["id"] for step in spec["steps"]}
        if step_id not in known_ids:
            fail(f"Unknown step id: {step_id}")
        step_state = state["steps"].setdefault(step_id, {})
        step_state.setdefault("status", "pending")
        step_state.setdefault("checkpoints", {})
        if args.json_file:
            payload = load_json(Path(args.json_file).resolve())
        else:
            try:
                payload = json.loads(args.json)
            except json.JSONDecodeError as exc:
                fail(f"Invalid --json payload: {exc}")
        if not isinstance(payload, dict):
            fail("Checkpoint payload must be a JSON object.")
        step_state["checkpoints"] = deep_merge(step_state["checkpoints"], payload)
        step_state["updated_at"] = now_iso()
        state["updated_at"] = now_iso()
        write_json(state_path, {k: v for k, v in state.items() if k != "_state_path"})
        print(f"Checkpoint updated for step `{step_id}`.")
        return 0

    if args.command in {"run", "verify"}:
        selected = select_steps(
            spec,
            getattr(args, "step", None),
            getattr(args, "from_step", None),
            getattr(args, "to_step", None),
        )
        verify_only = args.command == "verify" or getattr(args, "verify_only", False)
        for step in selected:
            ok, step_state = run_step(
                step=step,
                state=state,
                cwd=cwd,
                artifacts_root=artifacts_root,
                verify_only=verify_only,
                fail_closed=fail_closed,
                context_base=context,
            )
            state["steps"][step["id"]] = step_state
            state["updated_at"] = now_iso()
            write_json(state_path, {k: v for k, v in state.items() if k != "_state_path"})
            print(f"{step['id']}: {step_state.get('status')}")
            if step_state.get("failure_reason"):
                print(f"  reason: {step_state['failure_reason']}")
            if not ok and fail_closed:
                return 2
        return 0

    if args.command == "status":
        print_status(spec, state)
        return 0

    fail(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
