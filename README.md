# Syncause Debug Skill

AI can write code fast, but it still debugs like it’s blind: it only sees static files and whatever you paste into chat.

**Without Syncause**, coding agents often guess and only fix symptoms, so you may need to prompt the agent multiple times to fix the root cause.

**With Syncause**, agents can fix the root cause in one go. The Syncause debug skill lets your AI agent pull **runtime facts**—stack traces, request params, function inputs/outputs, key variable snapshots, and timelines—so fixes are based on **what actually happened**, not guesses.

This skill is a mandatory instruction set that constrains and guides the Agent's behavior:

- Mandatory Evidence Gathering: Before offering a fix, the Agent must call the MCP to fetch the Runtime Facts from the moment the bug occurred.
- Evidence-Based Repair: When analyzing the issue, the Agent is required to explicitly cite specific data points (e.g., "According to the stack trace, variable user_id was null at line 42...").
- No More Guessing: This fundamentally prevents the AI from "hallucinating code" when it lacks context.

## Typical use cases
- “It looks correct but still breaks” bugs
- Flaky failures that only show up at runtime
- Request/response mismatch, unexpected inputs, wrong state transitions
- Regressions after an AI-generated change

## Installation
### Automatic Installation

Install the skill for your AI agents with a single command:

```bash
npx skills add Syncause/debug-skill
```

This skill depends on the [Syncause MCP server](https://github.com/Syncause/mcp-server), which will be automatically installed when your agents use this skill. If the installation fails, you will be prompted to install it manually.

### Manual Installation
If your agent isn't automatically detected in the automatic installation process, please follow the manual setup guides below:

<details>
<summary><b>Cursor</b></summary>

#### Step 1: Skill installation

**Prompt-guided installation**
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .cursor/skills/ directory
- Global: Install to the ~/.cursor/skills/ directory
```

#### Step 2: MCP installation


#### One-Click Deeplink Installation
[![Install in Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en/install-mcp?name=debug-mcp-server&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBzeW5jYXVzZS9kZWJ1Zy1tY3BAbGF0ZXN0Il19Cg==)

**Or,** manually edit `.cursor/mcp.json` (project-level) or `~/.cursor/mcp.json` (global):
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

</details>

<details>
<summary><b>VS Code (GitHub Copilot Chat)</b></summary>

#### Step 1: Skill installation

> [!IMPORTANT]
> Ensure that:
> 1. The GitHub Copilot Chat extension is installed.
> 2. `chat.useAgentSkills` is enabled in settings.

**Prompt-guided installation**
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .github/skills/ directory
- Global: Install to the ~/.copilot/skills/ directory
```

#### Step 2: MCP installation


#### One-Click Deeplink Installation
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https%3A%2F%2Finsiders.vscode.dev%2Fredirect%2Fmcp%2Finstall%3Fname%3Ddebug-mcp-server%26config%3D%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40syncause%2Fdebug-mcp%40latest%22%5D%7D%7D)

**Or,** manually edit `.vscode/settings.json`:
```json
{
  "servers": {
    "debug-mcp-server": {
      "command": "npx",
      "args": ["-y", "@syncause/debug-mcp@latest"]
    }
  }
}
```

</details>

<details>
<summary><b>Claude Code</b></summary>

#### Step 1: Skill installation

**Prompt-guided installation**
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .claude/skills/ directory
- Global: Install to the ~/.claude/skills/ directory
```

#### Step 2: MCP installation


**CLI command (recommended)**
```bash
# Project-level
claude mcp add --scope project debug-mcp-server -- npx -y @syncause/debug-mcp@latest

# User-level
claude mcp add --scope user debug-mcp-server -- npx -y @syncause/debug-mcp@latest
```

**Or,** manually edit `.mcp.json` (project-level) or `~/.claude/settings.json` (user-level):
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

</details>

<details>
<summary><b>Codex</b></summary>

#### Step 1: Skill installation

**Prompt-guided installation**
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .codex/skills/ directory
- Global: Install to the ~/.codex/skills/ directory
```

#### Step 2: MCP installation


**CLI command (recommended)**
```bash
codex mcp add debug-mcp-server --command "npx -y @syncause/debug-mcp@latest"
```

**Or,** manually edit `~/.codex/config.toml`:
```toml
[mcp_servers.debug-mcp-server]
command = "npx"
args = ["-y", "@syncause/debug-mcp@latest"]
```

</details>

<details>
<summary><b>Gemini CLI</b></summary>

#### Step 1: Skill installation

**CLI command (recommended)**
```bash
# Project-level
gemini skills install https://github.com/Syncause/debug-skill.git --path skills/syncause-debugger --scope workspace

# Global
gemini skills install https://github.com/Syncause/debug-skill.git --path skills/syncause-debugger
```

**Or,** run the following in the Agent chat window within your terminal:
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .gemini/skills/ directory
- Global: Install to the ~/.gemini/skills/ directory
```

#### Step 2: MCP installation


**CLI command (recommended)**
```bash
gemini mcp add debug-mcp-server npx -y @syncause/debug-mcp@latest

**Or,** manually edit `.gemini/settings.json` (project-level) or `~/.gemini/settings.json` (global):
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

</details>

<details>
<summary><b>Antigravity</b></summary>

#### Step 1: Skill installation

**Prompt-guided installation**
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .agent/skills/ directory
- Global: Install to the ~/.gemini/antigravity/global_skills/ directory
```

#### Step 2: MCP installation


**Manually edit configuration**

1. Open the Agent sidebar in the Editor or the Agent Manager view
2. Click the “…” (More Actions) menu and select MCP Servers
3. Select View raw config to open `mcp_config.json` file
4. Add the following configuration:
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
5. Save the file and click Refresh in the MCP panel to see the new tools

</details>

<details>
<summary><b>Windsurf</b></summary>

#### Step 1: Skill installation

**Prompt-guided installation**
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .windsurf/skills/ directory
- Global: Install to the ~/.codeium/windsurf/skills/ directory
```

#### Step 2: MCP installation


**Manually edit configuration**
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

</details>

<details>
<summary><b>OpenCode</b></summary>

#### Step 1: Skill installation

**Prompt-guided installation**
```text
Help me install the Agent Skill: syncause-debugger
GitHub: https://github.com/Syncause/debug-skill/tree/main/skills/syncause-debugger

Please confirm the installation scope:
- Project-level: Install to the .opencode/skills/ directory
- Global: Install to the ~/.config/opencode/skills/ directory
```

> [!TIP]
> OpenCode is also compatible with Claude's skill directories: `.claude/skills/` and `~/.claude/skills/`

#### Step 2: MCP installation


**Manually edit configuration**
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

</details>

---

## Appendix

### Skill directory summary

| IDE         | Project-level Path  | Global Path                            |
| ----------- | ------------------- | -------------------------------------- |
| Cursor      | `.cursor/skills/`   | `~/.cursor/skills/`                    |
| VSCode      | `.github/skills/`   | `~/.copilot/skills/`                   |
| Claude Code | `.claude/skills/`   | `~/.claude/skills/`                    |
| Codex       | `.codex/skills/`    | `~/.codex/skills/`                     |
| Gemini CLI  | `.gemini/skills/`   | `~/.gemini/skills/`                    |
| Antigravity | `.agent/skills/`    | `~/.gemini/antigravity/global_skills/` |
| Windsurf    | `.windsurf/skills/` | `~/.codeium/windsurf/skills/`          |
| OpenCode    | `.opencode/skills/` | `~/.config/opencode/skills/`           |
