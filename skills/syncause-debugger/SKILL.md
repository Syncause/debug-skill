---
name: syncause-debugger
description: >
  Use runtime traces to diagnose and fix bugs. Enforces
  Reproduce → Classify → Trace-Driven Analysis → Precise Fix → Validate → Submit.
  Never bypass gates or lower standards to hide problems.
---

# Syncause Debugger

Use runtime traces to enhance bug fixing: collect runtime data with the SDK,
then analyze with MCP tools to drive hypothesis-based root cause analysis.

**Core discipline: never "solve" a problem by lowering standards.**
Gate rejection = signal, not obstacle. Find the real cause behind the rejection.

```
Setup → Reproduce & Baseline → Classify & Analyze → Fix → Validate → Submit → Teardown
```

---

## Phase 1: Setup

### Pre-check

1. **MCP Server**: This skill depends on `debug-mcp-server` MCP server. If it is not present, **STOP** and request the user to install the MCP server ([Anonymous Mode (Default)](./references/install/mcp-install-anonymous.md) or [Login Mode](./references/install/mcp-install-login.md)).
2. **Authentication**: If any MCP Tool returns a `Unauthorized` error, **STOP** and request the user to configure the `API_KEY` ([Login Mode Guide](./references/install/mcp-install-login.md)).

Verify SDK NOT already installed by checking dependency files:
- Java: `pom.xml` or `build.gradle`
- Node.js: `package.json`
- Python: `requirements.txt` or `pyproject.toml`

**WARNING:** `.syncause` folder is NOT a reliable indicator.

### Steps
1. **Initialize Project**: Use `setup_project(projectPath)` to get the `projectId`, `apiKey`, and `appName`.
   - **WARNING:** If tool not found or returns `Unauthorized`, **STOP** and follow [Pre-check](#pre-check).
2. **Install SDK**: Follow language guide:
   - [Java](./references/install/java.md)
   - [Node.js](./references/install/nodejs.md)
   - [Python](./references/install/python.md)
3. **Verify install**: Re-read dependency file to confirm SDK added
4. **Restart service**: Prefer starting new instance on different port over killing process

---

## Phase 2: Reproduce & Baseline

> **Reproduce the bug first, then establish a happy path baseline.
> Both are foundations for all downstream analysis.**

### 2.1 Study Existing Tests

Before writing anything, find existing tests for the affected module:
```bash
find <project> -path "*/test*" -name "*.py" | xargs grep -l "<keyword>" 2>/dev/null | head -10
```
Read 1-2 relevant tests. Extract key `(input, expected_output)` pairs. Your fix MUST pass these.

### 2.2 Define Behavior Contract

Write a compact contract table:

```
FUNCTION: <the function to fix>
| Input | Current (buggy) | Correct | Source |
1. Bug case from issue → Source = "issue"
2. 1-2 existing test cases → Source = "test: test_name"
3. 1 guard case (correct behavior) → Source = "guard"
```

### 2.3 Choose Reproduction Level

| Level | When | Example |
|-------|------|---------|
| **1 (best)** | User entry point available | `POST /api/login`, `call_command('migrate')` |
| **2** | Issue specifies exact internal params | `service.authenticate(args)` |
| **3 (worst)** | Upper layers impractical | Direct internal function call |

**Exception**: If the issue specifies parameters that differ from the user command, use Level 2.

### 2.4 Create Scripts

**`reproduce_issue.py`**:
```python
import sys
def run_reproduction_scenario():
    # 1. Setup: use project standard methods
    # 2. Trigger: execute the operation from the issue
    # 3. Verify: assertions for EVERY contract row
    if bug_detected:
        print("BUG_REPRODUCED: [message]")
        sys.exit(1)
    else:
        print("BUG_NOT_REPRODUCED")
        sys.exit(0)
if __name__ == "__main__":
    run_reproduction_scenario()
```

**`happy_path_test.py`**:
- MUST import and call actual project code
- MUST PASS before fix — only test already-correct behavior
- Do NOT include bug cases
- Use assert statements. At least 3 assertions
- Print `"HAPPY_PATH_SUCCESS"` after all pass

**Forbidden**: ❌ Mock classes ❌ Manual `sys.path` ❌ Isolated tempdir projects

### 2.5 Execute & Collect Trace

1. Run `reproduce_issue.py` to confirm bug exists
2. Collect trace: `search_debug_traces(projectId, query="keyword", limit=1)`
3. Get call tree: `get_trace_insight(projectId, traceId)` → find `[ERROR]` nodes

### 2.6 Run Happy Path BEFORE Edits

⚠️ **MANDATORY**: Run `happy_path_test.py` BEFORE any code edits. The baseline is lost if you edit first.

### 2.7 Quality Gate

```
✓ reproduce_issue consistently triggers bug (non-zero exit)
✓ happy_path_test passes (zero exit)
✓ Trace data contains error stack and key variable values
✓ Error type and location match bug description
```

---

## Phase 3: Classify & Analyze

> **Don't fix the first error you see. Classify the bug, then use
> trace data to systematically find root cause.**

### 3.1 Bug Classification (MANDATORY)

| Bug Class | Definition | Fix Location |
|-----------|-----------|--------------|
| **wrong-arg** | Function received value that SHOULD HAVE BEEN resolved upstream | Fix UPSTREAM (NOT crash site) |
| **missing-handler** | Function is correct place to handle this, but lacks handler | Add handler in crashing function |
| **logic** | Function's own code is wrong | Fix the function itself |

⚠️ **Disambiguation** (answer BEFORE choosing):
When crash involves unresolved/raw value (string ref, None):
- Q: Does the codebase have code that RESOLVES this value before it reaches here?
- YES → `wrong-arg` (resolve step was SKIPPED)
- NO → `missing-handler` (no resolve step exists)

### 3.2 Wrong-Arg: 5-Whys Tracing

If bug_class = wrong-arg, trace the producer of the wrong value **one WHY at a time**:

```
WHY_1: Where is this value SET or PASSED?
  → grep for parameter, classify each hit: SETTER vs READER

WHY_2: Read the SETTER. Which line passes the wrong variable?

WHY_3: Classify setter as:
  - 🔴 PRODUCER (computes value) → bug IS HERE
  - ⚪ CARRIER (forwards unchanged) → value already wrong
  - ⚫ CONSUMER (reads/checks) → NOT a producer

WHY_4: Open the PRODUCER, read the function
  → "This code processes the value by <how>"
  → "The value is wrong because <reason>"

WHY_5: Will fixing this DIRECTLY fix the parameter?
  → If fix uses hasattr/isinstance/try-except → NO (that's a guard, not root cause)
```

⚠️ Do NOT answer all WHYs at once. Each needs its own investigation.

### 3.3 Form Competing Hypotheses

Use trace data. Form at least 2 hypotheses with **different root causes**:

```
## Hypothesis h1
bug_class: <wrong-arg | missing-handler | logic>
claim: <root cause belief>
code_anchor: <file/function/line>
trace_anchor: <signal in trace>
prediction: <if true, what will trace show?>
falsifier: <what would DISPROVE this?>
verify_cmd: <trace verification command>
status: open
```

### 3.4 Verify with Trace Data

Use MCP tools to verify EVERY hypothesis:

```
search_debug_traces(projectId, query="<symptom>") → traceId
get_trace_insight(projectId, traceId) → find [ERROR] node
inspect_method_snapshot(projectId, traceId, className, methodName) → check args/return
diff_trace_execution(projectId, baseTraceId, compareTraceId) → compare fail vs success
```

Or local analysis:
```bash
python scripts/runtime_analyzer.py .syncause-cache/syncause_debug_.bin
```

### 3.5 Analysis Gate

**Code edits are BLOCKED until:**

```
✓ ≥ 2 competing hypotheses (different root causes)
✓ ≥ 1 supported (with trace evidence)
✓ ≥ 1 rejected (with actual command output, not theory)
✓ Happy path baseline captured
✓ Reproduce script validated
```

⚡ **FAST PATH**: Once you have ≥1 supported + ≥1 rejected → go to fix.
More reading after this is procrastination.

---

## Phase 4: Precise Fix

### 4.1 Fix Classification (MANDATORY)

**Classify every change BEFORE implementing:**

| Class | Definition | Allowed? |
|-------|-----------|----------|
| **A: Fix bug** | Logic error, missing handling, data issue | ✅ Yes |
| **B: Lower standards** | Lower threshold, weaken condition, skip check | ❌ **Needs user confirmation** |
| **C: Infrastructure** | Timeout guard, retry, error handling, logging | ✅ Yes |
| **D: Guidance** | Improve prompts, feedback messages, context | ✅ Yes |

### 4.2 B-Class Detection

**Any of these = B-class:**
- Lower numerical threshold (`0.3 → 0.2`)
- Reduce penalty value (`-0.7 → -0.15`)
- Add `if count > N: bypass` logic
- Comment out or delete checks
- Add `try/except: pass` to swallow errors
- Add `isinstance`/`hasattr` guard at crash site instead of fixing producer

**If B-class**: Stop → inform user → analyze A-class alternative → only implement after user confirms.

### 4.3 Fix Location Check

1. **Am I fixing CRASH SITE or ROOT CAUSE?** If adding guard → investigate deeper.
2. **Run `callers <function>`** — multiple callers? Fix PRODUCER, not each consumer.
3. **Is my diff minimal?** Prefer removing complexity over adding.
4. **Semantic check**: Does fix change how function interprets inputs? Trace each existing test through fix.

### 4.4 Fix Principles

| Principle | Rule |
|-----------|------|
| Minimal | Only change what must change |
| General | Fix must work for all similar cases, no hardcoding |
| No side-effects | Fix must not break existing behavior |
| Verifiable | Must have test proving effectiveness |
| Root cause | wrong-arg → fix upstream PRODUCER; missing-handler → add handler; logic → fix function |

---

## Phase 5: Validate & Iterate

> **Fix ≠ done. Must pass validation loop to confirm effectiveness.**

### 5.1 Validation Pipeline

```
Fix → verify edit correct → reproduce_issue → happy_path → project tests → diff review → confirmed
 ↑                                                                                    ↓
 ←←←←←←←←←←←←←←←←←←← Failed? Analyze and correct ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### 5.2 Validation Steps (ALL mandatory)

**Step 1**: Update `reproduce_issue.py` with correct expected values:
```bash
python3 reproduce_issue.py   # → exit 0 (bug fixed)
```

**Step 2**: Happy path verification:
```bash
python3 happy_path_test.py   # → HAPPY_PATH_SUCCESS
```
Collect post-fix trace and compare with pre-fix baseline.

**Step 3**: Trace verification (recommended):
```
search_debug_traces(projectId, query="<same symptom>", limit=1) → newTraceId
diff_trace_execution(projectId, baseTraceId=preFixTraceId, compareTraceId=newTraceId)
```

**Step 4**: Diff review:
```bash
git diff
```
Check: right file, minimal diff, no debug prints.

**Step 5**: Project tests:
```bash
python -m pytest <test_file> -x -q 2>&1 | tail -50
```

**If project test fails:**
1. Read failing test. What input/expected?
2. Asserting BUGGY output → update expected value only (write rationale)
3. Asserting CORRECT behavior → fix is incomplete, go back
4. Re-run ALL validations

### 5.3 Test Modification Policy

DEFAULT: Do not modify tests.

EXCEPTION — test asserts BUGGY output:
1. Complete code fix WITHOUT touching tests
2. Run tests, record failures
3. For each, write rationale: test name, old expected, why wrong, new value
4. ONLY change expected values
5. Never delete, skip, comment out, @xfail, or weaken tests

### 5.4 Iteration Rules

| Situation | Action |
|-----------|--------|
| reproduce still fails | **Back to Phase 3** — root cause may be wrong |
| happy_path fails | Fix has side-effects, check baseline comparison |
| project test fails | Distinguish: test asserts buggy output vs fix incomplete |
| All pass | Proceed to Phase 6 |

Max 3 iterations per fix approach. After 3 failures → back to Phase 3 for re-analysis.

---

## Phase 6: Submit & Summary

### 6.1 Submit

Once ALL validations pass, submit immediately. Do NOT clean up or delete any files.

### 6.2 Summary

**Required** summary after submitting:

1. **Root Cause**: Exact state/value that caused failure. How **Syncause** runtime visibility was key.
2. **Bug Classification**: State bug_class and how it determined fix strategy.
3. **Verification Results**:
   ```
   ✓ reproduce_issue exits code 0 (bug fixed)
   ✓ happy_path_test passes (baseline OK)
   ✓ Project tests: X passed, 0 failed
   ✓ Post-fix trace confirms error eliminated
   ```

---

## Phase 7: Teardown

**Required** after debugging to restore performance.

1. **Uninstall SDK**: Follow language guide:
   - [Java](./references/uninstall/java.md)
   - [Node.js](./references/uninstall/nodejs.md)
   - [Python](./references/uninstall/python.md)
2. **Delete** `.syncause` folder from project root

---

## Anti-Patterns (Strictly Forbidden)

| # | Anti-Pattern | Why Wrong | Correct Approach |
|---|-------------|-----------|-----------------|
| 1 | Fix crash site immediately | May be symptom not cause | Bug classification + 5-Whys to root cause |
| 2 | Add try/except to hide error | Masks the problem | Fix the root cause of the exception |
| 3 | Add isinstance/hasattr guard | B-class: hides wrong-arg | Find PRODUCER, fix the wrong value |
| 4 | Lower threshold to pass test | B-class fix | Investigate why threshold isn't met |
| 5 | Delete failing test | Hiding failure | Fix code to pass the test |
| 6 | No hypothesis before editing | May fix wrong location | ≥2 hypotheses, verify with trace, then fix |
| 7 | Reject hypothesis by theory | Lacks evidence | Rejection must cite actual command output |
| 8 | Change too many things at once | Can't isolate what worked | Minimal change, stepwise validation |
| 9 | Submit without testing | May introduce new bugs | Full validation pipeline |
| 10 | Read code endlessly without acting | Procrastination | Once hypothesis supported → fix immediately |
