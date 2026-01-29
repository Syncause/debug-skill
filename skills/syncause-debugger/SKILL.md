---
name: syncause-debugger
description: Debug and fix bugs using runtime traces. Supported Python, Node.js, Java ONLY.
---

# Syncause Debugger

Runtime trace-based debugging. 3 phases: Setup → Analyze → Teardown.



## Critical Pre-checks

1. **MCP Server**: This skill depends on `syncause-debugger-server` MCP server. If it is not present, **STOP** and request the user to install the MCP server ([Installation Guide](./references/install/mcp-install.md)).
2. **Authentication**: If any MCP Tool returns a `401 Unauthorized` error, **STOP** and request the user to configure the `API_KEY` ([Installation Guide](./references/install/mcp-install.md)).

## Phase 1: Setup

### Pre-check
Verify SDK NOT already installed by checking dependency files:
- Java: `pom.xml` or `build.gradle`
- Node.js: `package.json`
- Python: `requirements.txt` or `pyproject.toml`

⚠️ `.syncause` folder is NOT a reliable indicator.

### Steps
1. **Get credentials**: `get_project_id(projectPath)` → returns `projectId`, `apiKey`, `appName`
2. **Install SDK**: Follow language guide:
   - [Java](./references/install/java.md)
   - [Node.js](./references/install/nodejs.md)
   - [Python](./references/install/python.md)
3. **Verify install**: Re-read dependency file to confirm SDK added
4. **Restart service**: Prefer starting new instance on different port over killing process
5. **Reproduce bug**: Trigger the issue to generate trace data

## Phase 2: Analyze & Fix

```
# Step 1: Find trace
search_debug_traces(query="<symptom>") → pick traceId

# Step 2: Get call tree
get_trace_insight(traceId) → find ❌ [ERROR] node

# Step 3: Inspect method
inspect_method_snapshot(traceId, methodName) → check args/return/logs

# Step 4 (optional): Compare traces
diff_trace_execution(baseTraceId) → compare fail vs success
```

**Fix**: Edit code based on findings, re-run to verify.

⚠️ No traces? → Return to Phase 1, ensure SDK active and bug reproduced.

## Phase 3: Teardown

**REQUIRED** after debugging to restore performance.

1. **Uninstall SDK**: Follow language guide:
   - [Java](./references/uninstall/java.md)
   - [Node.js](./references/uninstall/nodejs.md)
   - [Python](./references/uninstall/python.md)
2. **Delete** `.syncause` folder from project root
