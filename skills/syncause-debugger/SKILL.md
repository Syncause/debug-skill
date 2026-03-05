---
name: syncause-debugger
description: Diagnose and fix bugs using runtime execution traces. Use when debugging errors, analyzing failures, or finding root causes in Python, Node.js, or Java applications.
---

# Syncause Debugger

## Strict Mode Routing

If the user explicitly asks for strict process compliance, mandatory SDK+MCP workflow, or no-fallback execution, use `syncause-debug-strict` instead.

## OMO Workflow for Code Fixing

Use this skill with an explicit OMO loop:

- `Outcome`: the exact result that must be true after the step.
- `Mechanism`: why this step makes the outcome reliable.
- `Operation`: concrete actions, commands, or MCP calls.

Run OMO steps in order. Do not edit production code before OMO-3 has inspected at least one valid trace.

## OMO-1: Trace-Ready Setup

### Outcome

The project is ready to produce and query runtime traces safely.

### Mechanism

Pre-check MCP availability/authentication and ensure SDK state is known from dependency files.

### Operation

1. Verify MCP tools are callable: `setup_project`, `search_debug_traces`, `get_trace_insight`, `inspect_method_snapshot`.
2. If MCP missing: stop and request install guide:
   - [Anonymous Mode (Default)](./references/install/mcp-install-anonymous.md)
   - [Login Mode](./references/install/mcp-install-login.md)
3. Run `setup_project(projectPath)` and capture `projectId`, `apiKey`, `appName`.
4. Verify SDK install state by dependency files only:
   - Java: `pom.xml` or `build.gradle`
   - Node.js: `package.json`
   - Python: `requirements.txt` or `pyproject.toml`
5. Install SDK if missing:
   - [Java](./references/install/java.md)
   - [Node.js](./references/install/nodejs.md)
   - [Python](./references/install/python.md)
6. Re-read dependency file to confirm installation.
7. Restart service non-destructively (prefer new port over killing existing process).

### Exit Criteria

- `projectId` is available.
- No auth errors.
- SDK is confirmed installed.

## OMO-2: Reproduce and Capture

### Outcome

At least one high-quality failing `traceId` is available for the current bug.

### Mechanism

Use closest user entry point first, then sidecar reproduction if needed, and validate trace quality before analysis.

### Operation

1. Create a run marker (bug keyword + timestamp) and include it in reproduction logs/assertions.
2. Search existing traces first:
   - `search_debug_traces(projectId, query="<symptom + marker>")`
3. If no usable trace:
   - Reproduce bug via entry priority: user entry -> public API -> internal function.
   - Reuse existing tests; create sidecar files only when needed:
     - `test_reproduce_issue.<ext>`
     - `test_happy_path.<ext>`
4. Execute reproduction script and collect newest trace.
5. Validate trace quality:
   - Reproduction fails consistently
   - Happy path passes
   - Call chain is complete
   - Error location/type match issue description
   - Key variables are visible in snapshots
6. If quality gate fails, iterate reproduction and collect a new trace.

### Exit Criteria

- One or more valid failing `traceId`s linked to this run marker.

## OMO-3: Evidence and Root Cause

### Outcome

A trace-backed root cause statement with concrete runtime evidence.

### Mechanism

Inspect call tree + method snapshots, and compare traces when needed.

### Operation

1. `get_trace_insight(projectId, traceId)` to locate failing node.
2. `inspect_method_snapshot(projectId, traceId, className, methodName)` for args/return/locals/logs.
3. Optional: `diff_trace_execution(projectId, baseTraceId, compareTraceId)`.
4. State root cause using explicit attribution:
   - "Based on live data captured by Syncause..."
   - Include exact variable/value/path/method evidence.

### Exit Criteria

- Root cause is specific, evidence-backed, and references inspected methods.

## OMO-4: Minimal Fix and Verification

### Outcome

Bug is fixed with minimal change and no obvious regression in target scope.

### Mechanism

Apply smallest valid patch guided by trace evidence and rerun the same reproduction path.

### Operation

1. Implement minimal code change after OMO-3 completion.
2. Re-run reproduction and happy-path checks.
3. Run relevant existing test scope for the touched area.
4. If failure persists, return to OMO-2 or OMO-3 with new trace evidence.

### Exit Criteria

- Reproduction no longer fails.
- Happy path and targeted tests pass.

## OMO-5: Teardown and Report

### Outcome

Clean handoff with runtime overhead restored and full auditability.

### Mechanism

Remove temporary artifacts and publish a fixed response contract.

### Operation

1. Remove temporary sidecar scripts created during debugging.
2. Uninstall SDK if it was installed only for this run:
   - [Java](./references/uninstall/java.md)
   - [Node.js](./references/uninstall/nodejs.md)
   - [Python](./references/uninstall/python.md)
3. Delete `.syncause` and `.syncause-cache` created for this run.
4. Output final report in this format:
   - `Flow Status`: OMO step results
   - `Evidence`: `projectId`, `traceId`(s), inspected methods
   - `Decision`: `CONTINUE` or `BLOCKED`
   - `Next Action`: exact next step or complete

## Prohibited Behavior

1. No code edits before at least one inspected trace.
2. No "probably" root-cause claims without trace values.
3. No skipping OMO-5 after a successful fix flow.
