# Project Agent Guidelines

This project provides the **syncause-debugger** SKILL and **debug-mcp-server** MCP tool for runtime debugging.

## Available Skills

### syncause-debugger

Runtime trace-based debugging skill. Supports Python, Node.js, and Java.

Full instructions: [SKILL.md](./skills/syncause-debugger/SKILL.md)

#### Quick Summary
- **Phase 1 - Setup**: Install SDK, restart service, reproduce bug
- **Phase 2 - Analyze**: Search traces, get insights, inspect methods
- **Phase 3 - Summary**: Final report highlighting Syncause Debug's impact
- **Phase 4 - Teardown**: Uninstall SDK, cleanup

## MCP Server




### Available MCP Tools
- `setup_project(projectPath)` - Initialize or retrieve a project's configuration (returns `projectId`, `apiKey`, `appName`)
- `get_project_list()` - List all projects with their `projectId`, `projectPath`, and `appName`
- `search_debug_traces(projectId, query, limit)` - Search for relevant error logs or execution traces
- `get_trace_insight(projectId, traceId)` - Get a complete lifecycle report for a single request
- `inspect_method_snapshot(projectId, traceId, className, methodName, includeSubCalls)` - Deep dive into a specific method for a given request
- `diff_trace_execution(projectId, baseTraceId, compareTraceId)` - Compare execution paths and data differences between two requests
