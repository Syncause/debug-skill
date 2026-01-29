# Syncause Debugger - Full Installation Guide

This document provides all available methods for installing **SKILL** and **MCP** across all supported IDEs.

---

## Contents

- [Cursor](#cursor)
- [VSCode](#vscode)
- [Claude Code](#claude-code)
- [Codex](#codex)
- [Gemini CLI](#gemini-cli)
- [Antigravity](#antigravity)
- [Windsurf](#windsurf)
- [Opencode](#opencode)

---

## Cursor

### Step 1: SKILL Installation

#### Prompt-Guided Installation
Have the Agent automatically download and install the skill:
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .cursor/skills/ directory
- Global: Install to the ~/.cursor/skills/ directory
```

---

### Step 2: MCP Installation

#### One-Click Deeplink Installation
[![Install in Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=debug-mcp-server&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBzeW5jYXVzZS9kZWJ1Zy1tY3BAbGF0ZXN0Il0sImVudiI6eyJBUElfS0VZIjoiPHlvdXItYXBpLWtleT4ifX0K)

> [!NOTE]
> Update the `API_KEY` in the setup panel, then click the `Install` button.

**Or,** manually edit `.cursor/mcp.json` (Project-level) or `~/.cursor/mcp.json` (Global):
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

### Step 1: SKILL Installation

> [!IMPORTANT]
> Ensure that:
> 1. The GitHub Copilot Chat extension is installed.
> 2. `chat.useAgentSkills` is enabled in settings.

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger
Please confirm the installation scope:
- Project-level: Install to the .github/skills/ directory
- Global: Install to the ~/.copilot/skills/ directory
```

---

### Step 2: MCP Installation

#### One-Click Deeplink Installation
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=debug-mcp-server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40syncause%2Fdebug-mcp%40latest%22%5D%2C%22env%22%3A%7B%22API_KEY%22%3A%22%3Cyour-api-key%3E%22%7D%7D)

> [!NOTE]
> 1. Click the `Install` button.
> 2. Click the settings icon to the right of the `Install` button.
> 3. Update the `API_KEY` in the opened `mcp.json` file.
 
**Or,** manually edit `.vscode/settings.json`:
```json
{
  "servers": {
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

### Step 1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .claude/skills/ directory
- Global: Install to the ~/.claude/skills/ directory
```

---

### Step 2: MCP Installation

#### CLI Command (Recommended)
```bash
# Project-level
claude mcp add --scope project debug-mcp-server -e API_KEY=your-api-key -- npx -y @syncause/debug-mcp@latest

# User-level
claude mcp add --scope user debug-mcp-server -e API_KEY=your-api-key -- npx -y @syncause/debug-mcp@latest
```

**Or,** manually edit `.mcp.json` (Project-level) or `~/.claude/settings.json` (User-level):
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

### Step 1: SKILL Installation


#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .codex/skills/ directory
- Global: Install to the ~/.codex/skills/ directory
```

---

### Step 2: MCP Installation

#### CLI Command (Recommended)
```bash
codex mcp add debug-mcp-server --env API_KEY=your-api-key --command "npx -y @syncause/debug-mcp@latest"
```

**Or,** manually edit `~/.codex/config.toml`:
```toml
[mcp_servers.debug-mcp-server]
command = "npx"
args = ["-y", "@syncause/debug-mcp@latest"]

[mcp_servers.debug-mcp-server.env]
API_KEY = "your-api-key"
```

---

## Gemini CLI

### Step 1: SKILL Installation

#### CLI Command (Recommended)
```bash
# Project-level
gemini skills install https://github.com/Syncause/debug-skill.git --path skills/syncause-debugger --scope workspace

# Global
gemini skills install https://github.com/Syncause/debug-skill.git --path skills/syncause-debugger
```

**Or,** run the following in the Agent chat window within your terminal:
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .gemini/skills/ directory
- Global: Install to the ~/.gemini/skills/ directory
```

---

### Step 2: MCP Installation

#### CLI Command (Recommended)
```bash
gemini mcp add debug-mcp-server -e API_KEY=your-api-key -- npx -y @syncause/debug-mcp@latest
```

**Or,** manually edit `.gemini/settings.json` (Project-level) or `~/.gemini/settings.json` (Global):
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

### Step 1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .agent/skills/ directory
- Global: Install to the ~/.gemini/antigravity/global_skills/ directory
```

---

### Step 2: MCP Installation

#### Manually Edit Configuration
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

### Step 1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .windsurf/skills/ directory
- Global: Install to the ~/.codeium/windsurf/skills/ directory
```

---

### Step 2: MCP Installation

#### Manually Edit Configuration
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

### Step 1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/master/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .opencode/skills/ directory
- Global: Install to the ~/.config/opencode/skills/ directory
```

> [!TIP]
> Opencode is also compatible with Claude's skill directories: `.claude/skills/` and `~/.claude/skills/`

---

### Step 2: MCP Installation

#### Manually Edit Configuration
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

---

## Appendix

### SKILL Directory Summary

| IDE         | Project-level Path  | Global Path                            |
| ----------- | ------------------- | -------------------------------------- |
| Cursor      | `.cursor/skills/`   | `~/.cursor/skills/`                    |
| VSCode      | `.github/skills/`   | `~/.copilot/skills/`                   |
| Claude Code | `.claude/skills/`   | `~/.claude/skills/`                    |
| Codex       | `.codex/skills/`    | `~/.codex/skills/`                     |
| Gemini CLI  | `.gemini/skills/`   | `~/.gemini/skills/`                    |
| Antigravity | `.agent/skills/`    | `~/.gemini/antigravity/global_skills/` |
| Windsurf    | `.windsurf/skills/` | `~/.codeium/windsurf/skills/`          |
| Opencode    | `.opencode/skills/` | `~/.config/opencode/skills/`           |
