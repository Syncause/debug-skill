# Syncause Java Agent Uninstallation Guide

To uninstall the Java Agent and cleanup the project:

## 1. Delete Wrapper Scripts
Delete the `scripts/` directory or its contents related to the Syncause agent:
```bash
rm scripts/run_java_with_agent.sh scripts/run_java_with_agent.ps1
```

## 2. Cleanup Downloaded Agents (Optional)
The agent JAR is downloaded to `~/.syncause/agents/`. You can delete this directory to free up space:
```bash
rm -rf ~/.syncause/agents/
```

## 3. Remove .syncause Folder
Delete the `.syncause` folder from the project root:
```bash
rm -rf .syncause
```
