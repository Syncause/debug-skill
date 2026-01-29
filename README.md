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
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .cursor/skills/ directory
- Global: Install to the ~/.cursor/skills/ directory
```

---

### Step 2: MCP Installation

#### Method 1: One-Click Deeplink Installation
[<img src="https://img.shields.io/badge/Install%20to%20Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" />](cursor://anysphere.cursor-deeplink/mcp/install?name=debug-mcp-server&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBzeW5jYXVzZS9kZWJ1Zy1tY3BAbGF0ZXN0Il0sImVudiI6eyJBUElfS0VZIjoiPHlvdXItYXBpLWtleT4ifX0K)

> [!NOTE]
> Update the `API_KEY` in the setup panel, then click the `Install` button.

#### Method 2: Manually Edit Configuration
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

### Step1: SKILL Installation

> [!IMPORTANT]
> Ensure that:
> 1. The GitHub Copilot Chat extension is installed.
> 2. `chat.useAgentSkills` is enabled in settings.

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger
Please confirm the installation scope:
- Project-level: Install to the .github/skills/ directory
- Global: Install to the ~/.copilot/skills/ directory
```

---

### Step2: MCP Installation

#### Method 1: One-Click Deeplink Installation
[<img src="https://img.shields.io/badge/Install%20to%20VSCode-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white" />](vscode:mcp/install?%7B%22name%22%3A%22debug-mcp-server%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40syncause%2Fdebug-mcp%40latest%22%5D%2C%22env%22%3A%7B%22API_KEY%22%3A%22%3Cyour-api-key%3E%22%7D%7D)

> [!NOTE]
> 1. Click the `Install` button.
> 2. Click the settings icon to the right of the `Install` button.
> 3. Update the `API_KEY` in the opened `mcp.json` file.
 
#### Method 2: Manually Edit Configuration
Edit `.vscode/settings.json`:
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

### Step1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .claude/skills/ directory
- Global: Install to the ~/.claude/skills/ directory
```

---

### Step2: MCP Installation

#### Method 1: CLI Command (Recommended)
```bash
# Project-level
claude mcp add --scope project debug-mcp-server -e API_KEY=your-api-key -- npx -y @syncause/debug-mcp@latest

# User-level
claude mcp add --scope user debug-mcp-server -e API_KEY=your-api-key -- npx -y @syncause/debug-mcp@latest
```

#### Method 2: Manually Edit Configuration
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

### Step1: SKILL Installation


#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .codex/skills/ directory
- Global: Install to the ~/.codex/skills/ directory
```

---

### Step2: MCP Installation

#### Method 1: CLI Command (Recommended)
```bash
codex mcp add debug-mcp-server --env API_KEY=your-api-key --command "npx -y @syncause/debug-mcp@latest"
```

#### Method 2: Manually Edit Configuration
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

### Step1: SKILL Installation

#### Method 1: CLI Command (Recommended)
```bash
# Project-level
gemini skills install https://github.com/Syncause/debug-skill.git --path skills/syncause-debugger --scope workspace

# Global
gemini skills install https://github.com/Syncause/debug-skill.git --path skills/syncause-debugger
```

#### Method 2: Prompt-Guided Installation
Run the following command in the Agent chat window within your terminal:
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .gemini/skills/ directory
- Global: Install to the ~/.gemini/skills/ directory
```

---

### Step2: MCP Installation

#### Method 1: CLI Command (Recommended)
```bash
gemini mcp add debug-mcp-server -e API_KEY=your-api-key -- npx -y @syncause/debug-mcp@latest
```

#### Method 2: Manually Edit Configuration
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

### Step1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .agent/skills/ directory
- Global: Install to the ~/.gemini/antigravity/global_skills/ directory
```

---

### Step2: MCP Installation

#### Method 1: Manually Edit Configuration (Recommended)
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

### Step1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .windsurf/skills/ directory
- Global: Install to the ~/.codeium/windsurf/skills/ directory
```

---

### Step2: MCP Installation

#### Method 1: Manually Edit Configuration
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

### Step1: SKILL Installation

#### Prompt-Guided Installation
```
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .opencode/skills/ directory
- Global: Install to the ~/.config/opencode/skills/ directory
```

> [!TIP]
> Opencode is also compatible with Claude's skill directories: `.claude/skills/` and `~/.claude/skills/`

---

### Step2: MCP Installation

#### Method 1: Manually Edit Configuration
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
