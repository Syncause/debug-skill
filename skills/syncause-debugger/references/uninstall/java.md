# Syncause Java Agent Uninstallation Guide

To uninstall the Java Agent and cleanup the project, please complete the following steps:

<step_1>
### 1. Delete Wrapper Scripts
Delete the wrapper scripts that were added to your project. Remove the following files or the entire `scripts/` directory if it contains nothing else:
- `scripts/run_java_with_agent.sh`
- `scripts/run_java_with_agent.ps1`
</step_1>

<step_2>
### 2. Cleanup Downloaded Agents (Optional)
The agent JAR is downloaded to the user's home directory. You can delete this directory to free up space:
- `~/.syncause/agents/`
</step_2>

<step_3>
### 3. Remove .syncause Folder
Delete the internal `.syncause` configuration folder from the project root:
- `.syncause/`
</step_3>
