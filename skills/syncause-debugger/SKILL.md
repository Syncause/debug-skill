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

## Hard Gate Execution

When available, execute this skill with the gate runner to enforce fail-closed step checks:

1. Initialize gate state once per run:
   - `python3 .agent/skills/syncause-debug-skill/scripts/gate_runner.py --skill .agent/skills/syncause-debug-skill/SKILL.md --cwd . init`
2. After completing each OMO step, record evidence:
   - `python3 .agent/skills/syncause-debug-skill/scripts/gate_runner.py --skill .agent/skills/syncause-debug-skill/SKILL.md --cwd . checkpoint --step OMO-1 --json '{"mcpToolsCallable":true,"projectId":"<id>","auth":"ok","sdkInstalled":true}'`
3. Verify the step before proceeding:
   - `python3 .agent/skills/syncause-debug-skill/scripts/gate_runner.py --skill .agent/skills/syncause-debug-skill/SKILL.md --cwd . verify --step OMO-1`
4. If a verification fails, stop and report `BLOCKED`.
5. Check current status at any time:
   - `python3 .agent/skills/syncause-debug-skill/scripts/gate_runner.py --skill .agent/skills/syncause-debug-skill/SKILL.md --cwd . status`

Gate layers:

- `process`: order and step completion facts.
- `evidence`: trace IDs, inspected methods, and concrete runtime data.
- `change`: patch boundary and mutation safety.
- `quality`: repro/test outcomes and release confidence.

Each gate supports `mode: hard|soft`. Hard gate failure blocks progress; soft gate failure warns but does not block.

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
7. **MANDATORY GATE:** You MUST run the following command before starting OMO-3:
   `python ./scripts/omo_gatekeeper.py --gate omo2 --trace-id <Your_Found_Trace_Id>`
8. If the script exits with code 1 (REJECTED), you MUST stay in OMO-2 and try again. Do not proceed to OMO-3.

### Exit Criteria

- Gatekeeper script returns `[PASSED]`.
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
5. **MANDATORY GATE:** You MUST run the following command before starting OMO-4:
   `python ./scripts/omo_gatekeeper.py --gate omo3 --cause-file <File_To_Fix>`
6. If the script exits with code 1 (REJECTED), you MUST stay in OMO-3 and gather more evidence. Do not proceed to OMO-4 code edits.

### Exit Criteria

- Gatekeeper script returns `[PASSED]`.
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

## Gate Contract (Machine Readable)

The following JSON block is consumed by `scripts/gate_runner.py`.

```gate-spec-json
{
  "version": 1,
  "workflow": "syncause-debug-omo",
  "fail_closed": true,
  "steps": [
    {
      "id": "OMO-1",
      "title": "Trace-Ready Setup",
      "operations": [
        {
          "id": "setup-and-sdk-check",
          "type": "manual",
          "description": "Run MCP tool checks, setup_project(projectPath), and SDK install validation."
        }
      ],
      "gates": [
        {
          "id": "process",
          "mode": "hard",
          "verifiers": [
            {
              "id": "mcp-tools-callable",
              "type": "checkpoint_path_equals",
              "path": "mcpToolsCallable",
              "value": true
            }
          ]
        },
        {
          "id": "evidence",
          "mode": "hard",
          "verifiers": [
            {
              "id": "project-id-present",
              "type": "checkpoint_path_exists",
              "path": "projectId"
            },
            {
              "id": "auth-ok",
              "type": "checkpoint_path_equals",
              "path": "auth",
              "value": "ok"
            },
            {
              "id": "sdk-installed",
              "type": "checkpoint_path_equals",
              "path": "sdkInstalled",
              "value": true
            }
          ]
        },
        {
          "id": "change",
          "mode": "hard",
          "verifiers": [
            {
              "id": "no-new-git-changes",
              "type": "git_no_new_changes"
            }
          ]
        }
      ]
    },
    {
      "id": "OMO-2",
      "title": "Reproduce and Capture",
      "requires": [
        "OMO-1"
      ],
      "operations": [
        {
          "id": "reproduce-and-collect-trace",
          "type": "manual",
          "description": "Run reproduction path and collect failing traceId values."
        }
      ],
      "gates": [
        {
          "id": "process",
          "mode": "hard",
          "verifiers": [
            {
              "id": "run-marker-created",
              "type": "checkpoint_path_equals",
              "path": "runMarkerCreated",
              "value": true
            }
          ]
        },
        {
          "id": "evidence",
          "mode": "hard",
          "verifiers": [
            {
              "id": "failing-traceids",
              "type": "checkpoint_array_nonempty",
              "path": "failingTraceIds"
            },
            {
              "id": "call-chain-complete",
              "type": "checkpoint_path_equals",
              "path": "callChainComplete",
              "value": true
            },
            {
              "id": "key-variables-visible",
              "type": "checkpoint_path_equals",
              "path": "keyVariablesVisible",
              "value": true
            }
          ]
        },
        {
          "id": "quality",
          "mode": "hard",
          "verifiers": [
            {
              "id": "reproduction-failed",
              "type": "checkpoint_path_equals",
              "path": "reproductionFailed",
              "value": true
            },
            {
              "id": "happy-path-passed",
              "type": "checkpoint_path_equals",
              "path": "happyPathPassed",
              "value": true
            }
          ]
        },
        {
          "id": "change",
          "mode": "hard",
          "verifiers": [
            {
              "id": "no-new-git-changes",
              "type": "git_no_new_changes"
            }
          ]
        }
      ]
    },
    {
      "id": "OMO-3",
      "title": "Evidence and Root Cause",
      "requires": [
        "OMO-2"
      ],
      "operations": [
        {
          "id": "trace-analysis",
          "type": "manual",
          "description": "Inspect trace insight and method snapshots, then write trace-backed root cause."
        }
      ],
      "gates": [
        {
          "id": "process",
          "mode": "hard",
          "verifiers": [
            {
              "id": "trace-insight-inspected",
              "type": "checkpoint_path_equals",
              "path": "traceInsightInspected",
              "value": true
            }
          ]
        },
        {
          "id": "evidence",
          "mode": "hard",
          "verifiers": [
            {
              "id": "analysis-traceid-present",
              "type": "checkpoint_path_exists",
              "path": "traceId"
            },
            {
              "id": "inspected-methods",
              "type": "checkpoint_array_nonempty",
              "path": "inspectedMethods"
            },
            {
              "id": "root-cause-statement",
              "type": "checkpoint_path_exists",
              "path": "rootCauseStatement"
            },
            {
              "id": "evidence-values",
              "type": "checkpoint_array_nonempty",
              "path": "evidenceValues"
            }
          ]
        },
        {
          "id": "quality",
          "mode": "hard",
          "verifiers": [
            {
              "id": "syncause-attribution",
              "type": "checkpoint_path_equals",
              "path": "rootCauseAttributedToSyncause",
              "value": true
            }
          ]
        },
        {
          "id": "change",
          "mode": "hard",
          "verifiers": [
            {
              "id": "no-new-git-changes",
              "type": "git_no_new_changes"
            }
          ]
        }
      ]
    },
    {
      "id": "OMO-4",
      "title": "Minimal Fix and Verification",
      "requires": [
        "OMO-3"
      ],
      "operations": [
        {
          "id": "apply-fix-and-test",
          "type": "manual",
          "description": "Apply minimal patch, rerun reproduction/happy path, and run targeted tests."
        }
      ],
      "gates": [
        {
          "id": "process",
          "mode": "hard",
          "verifiers": [
            {
              "id": "fix-applied",
              "type": "checkpoint_path_equals",
              "path": "fixApplied",
              "value": true
            }
          ]
        },
        {
          "id": "change",
          "mode": "hard",
          "verifiers": [
            {
              "id": "minimal-patch",
              "type": "checkpoint_path_equals",
              "path": "minimalPatch",
              "value": true
            },
            {
              "id": "changed-files-recorded",
              "type": "checkpoint_array_nonempty",
              "path": "changedFiles"
            }
          ]
        },
        {
          "id": "quality",
          "mode": "hard",
          "verifiers": [
            {
              "id": "reproduction-now-passes",
              "type": "checkpoint_path_equals",
              "path": "reproductionNoLongerFails",
              "value": true
            },
            {
              "id": "happy-path-passed",
              "type": "checkpoint_path_equals",
              "path": "happyPathPassed",
              "value": true
            },
            {
              "id": "targeted-tests-passed",
              "type": "checkpoint_path_equals",
              "path": "targetedTestsPassed",
              "value": true
            }
          ]
        }
      ]
    },
    {
      "id": "OMO-5",
      "title": "Teardown and Report",
      "requires": [
        "OMO-4"
      ],
      "operations": [
        {
          "id": "teardown-and-report",
          "type": "manual",
          "description": "Remove sidecar files, cleanup Syncause artifacts, and output final report contract."
        }
      ],
      "gates": [
        {
          "id": "process",
          "mode": "hard",
          "verifiers": [
            {
              "id": "sidecars-removed",
              "type": "checkpoint_path_equals",
              "path": "sidecarsRemoved",
              "value": true
            },
            {
              "id": "runtime-artifacts-cleaned",
              "type": "checkpoint_path_equals",
              "path": "runtimeArtifactsCleaned",
              "value": true
            }
          ]
        },
        {
          "id": "evidence",
          "mode": "hard",
          "verifiers": [
            {
              "id": "flow-status-present",
              "type": "checkpoint_path_exists",
              "path": "finalReport.flowStatus"
            },
            {
              "id": "next-action-present",
              "type": "checkpoint_path_exists",
              "path": "finalReport.nextAction"
            }
          ]
        },
        {
          "id": "quality",
          "mode": "hard",
          "verifiers": [
            {
              "id": "decision-continue",
              "type": "checkpoint_path_equals",
              "path": "finalReport.decision",
              "value": "CONTINUE"
            }
          ]
        }
      ]
    }
  ]
}
```
