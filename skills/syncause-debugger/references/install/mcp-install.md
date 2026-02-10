# MCP Server Installation - Configuration Guide

This document provides the **configuration-only** method for installing the `@syncause/debug-mcp` MCP server.

You should modify the configuration file for your specific IDE. **Project-level** configuration is recommended where available.

If you can't modify the configuration file, you MUST output the instructions to the user, instead of letting the user read this document.

## Cursor

Edit `.cursor/mcp.json` (Project-level) or `~/.cursor/mcp.json` (Global):

```json
{
  "mcpServers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"]
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
      "args": ["-y", "@syncause/debug-mcp@latest"]
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
      "args": ["-y", "@syncause/debug-mcp@latest"]
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

```

---

## Gemini CLI

Edit `.gemini/settings.json` (Project-level) or `~/.gemini/settings.json` (Global):

```json
{
  "mcpServers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"]
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
      "args": ["-y", "@syncause/debug-mcp@latest"]
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
      "args": ["-y", "@syncause/debug-mcp@latest"]
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
      "enabled": true
    }
  }
}
```
