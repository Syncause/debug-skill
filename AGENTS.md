# Project Agent Guidelines

This project provides the **syncause-debugger** SKILL and **debug-mcp-server** MCP tool for runtime debugging.

## Available Skills

### syncause-debugger

Runtime trace-based debugging skill. Supports Python, Node.js, and Java.

Full instructions: [SKILL.md](./skills/syncause-debugger/SKILL.md)

#### Quick Summary
- **Phase 1 - Setup**: Install SDK, restart service, reproduce bug
- **Phase 2 - Analyze**: Search traces, get insights, inspect methods
- **Phase 3 - Teardown**: Uninstall SDK, cleanup

## MCP Server




### Available MCP Tools
- `get_project_id(projectPath)` - Get project credentials
- `search_debug_traces(query)` - Search for traces
- `get_trace_insight(traceId)` - Get call tree analysis
- `inspect_method_snapshot(traceId, methodName)` - Inspect method details
- `diff_trace_execution(baseTraceId)` - Compare traces
