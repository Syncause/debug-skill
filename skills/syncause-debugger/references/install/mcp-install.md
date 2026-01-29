# MCP Server Installation - Configuration Guide

This document provides the **configuration-only** method for installing the `syncause-debugger-server` MCP server.
You should modify the configuration file for your specific IDE. **Project-level** configuration is recommended where available.

---

## Cursor

Edit `.cursor/mcp.json` (Project-level) or `~/.cursor/mcp.json` (Global):

```json
{
  "mcpServers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"],
      "env": {
        "API_KEY": "<your-api-key>"
      }
    }
  }
}
```

---

## VSCode

Edit `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"],
      "env": { "API_KEY": "your-api-key" }
    }
  }
}
```

---

## Claude Code

Edit `.mcp.json` (Project-level) or `~/.claude/settings.json` (User-level):

```json
{
  "mcpServers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"],
      "env": { "API_KEY": "your-api-key" }
    }
  }
}
```

---

## Codex

Edit `~/.codex/config.toml`:

```toml
[mcp_servers.debug-mcp-server]
command = "npx"
args = ["-y", "@syncause/debug-mcp@latest"]

[mcp_servers.debug-mcp-server.env]
API_KEY = "your-api-key"
```

---

## Gemini CLI

Edit `.gemini/settings.json` (Project-level) or `~/.gemini/settings.json` (Global):

```json
{
  "mcpServers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"],
      "env": { "API_KEY": "your-api-key" }
    }
  }
}
```

---

## Antigravity

Edit `~/.gemini/antigravity/mcp_config.json` (Global):

```json
{
  "mcpServers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"],
      "env": { "API_KEY": "your-api-key" }
    }
  }
}
```

---

## Windsurf

Edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"],
      "env": { "API_KEY": "your-api-key" }
    }
  }
}
```

---

## Opencode

Edit `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "http://opencode.ai/config.json",
  "mcp": {
    "debug-mcp-server": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"],
      "environment": { "API_KEY": "your-api-key" },
      "enabled": true
    }
  }
}
```
