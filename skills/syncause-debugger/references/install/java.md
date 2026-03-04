# Syncause Java Agent Installation Guide

When tasked with installing the Java Agent into a project, follow this prioritized execution flow:

## 1. Identify Project Type
Detect if the project is using Maven (`pom.xml`), Gradle (`build.gradle` or `build.gradle.kts`), or Ant (`build.xml`).

## 2. Create Wrapper Scripts
To avoid manual configuration of `JAVA_TOOL_OPTIONS`, you MUST create wrapper scripts in the `scripts/` directory.

> [!IMPORTANT]
> **Multi-module Projects**: Create the `scripts/` directory in the same path used for `setup_project(projectPath)` (the specific module's root). All commands should then be executed from this directory.

### Step 2.1: Create `scripts/run_java_with_agent.sh` (for Linux/macOS/WSL)
Create the file and make it executable (`chmod +x scripts/run_java_with_agent.sh`).

```bash
#!/bin/bash
# Description: Wrapper to run any command (java, mvn, etc.) with the Syncause Agent loaded via JAVA_TOOL_OPTIONS locally.

# === CONFIGURATION (Maintainer: Update version here) ===
AGENT_VERSION="0.1.2"

# === ENVIRONMENT (Expected from setup_project) ===
if [ -z "$API_KEY" ] || [ -z "$APP_NAME" ] || [ -z "$PROJECT_ID" ]; then
  echo "ERROR: API_KEY, APP_NAME, and PROJECT_ID must be set in the environment."
  exit 1
fi

AGENT_DIR="$HOME/.syncause/agents"
AGENT_JAR="$AGENT_DIR/syncause-agent-$AGENT_VERSION.jar"

# Auto-download if doesn't exist
if [ ! -f "$AGENT_JAR" ]; then
    mkdir -p "$AGENT_DIR"
    URL="https://github.com/Syncause/syncause-sdk/releases/download/syncause_agent_v$AGENT_VERSION/syncause-agent-$AGENT_VERSION.jar"
    echo "Downloading Agent v$AGENT_VERSION for one-time run..."
    curl -L -o "$AGENT_JAR" "$URL"
fi

# Set local environment and exec
AGENT_OPTS="-javaagent:$AGENT_JAR=api_key=$API_KEY,project_name=$APP_NAME,project_id=$PROJECT_ID"
if [[ ! "$JAVA_TOOL_OPTIONS" == *"$AGENT_OPTS"* ]]; then
  export JAVA_TOOL_OPTIONS=$(echo "$JAVA_TOOL_OPTIONS $AGENT_OPTS" | xargs)
fi

# Execute the remaining command
# If the command was passed as a single quoted string (e.g., "mvn test"), 
# let the shell split it. Otherwise, preserve arguments exactly.
if [ $# -eq 1 ] && [[ "$1" == *" "* ]]; then
  exec $1
else
  exec "$@"
fi
```

### Step 2.2: Create `scripts/run_java_with_agent.ps1` (for Windows PowerShell)

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Command
)

# Description: Wrapper to run any command with the Syncause Agent loaded via JAVA_TOOL_OPTIONS locally.
# Usage: ./scripts/run_java_with_agent.ps1 "mvn test -Dtest=MyTest"

# === CONFIGURATION (Maintainer: Update version here) ===
$AGENT_VERSION = "0.1.2"

# === ENVIRONMENT (Expected from setup_project) ===
if (-not $env:API_KEY -or -not $env:APP_NAME -or -not $env:PROJECT_ID) {
    Write-Error "ERROR: API_KEY, APP_NAME, and PROJECT_ID must be set in the Environment."
    return
}

$agentDir = "$HOME\.syncause\agents"
$agentJar = Join-Path $agentDir "syncause-agent-$AGENT_VERSION.jar"

# Auto-download if doesn't exist
if (!(Test-Path $agentJar)) {
    if (!(Test-Path $agentDir)) { New-Item -ItemType Directory -Path $agentDir | Out-Null }
    $url = "https://github.com/Syncause/syncause-sdk/releases/download/syncause_agent_v$AGENT_VERSION/syncause-agent-$AGENT_VERSION.jar"
    Write-Host "Downloading Agent v$AGENT_VERSION for one-time run..."
    Invoke-WebRequest -Uri $url -OutFile $agentJar
}

# Build the agent option string
$agentOpts = "-javaagent:$agentJar=api_key=$env:API_KEY,project_name=$env:APP_NAME,project_id=$env:PROJECT_ID"

# Execute the command in a child process with JAVA_TOOL_OPTIONS set to ONLY the agent.
# Using cmd /c ensures the env var is local to this invocation and does not accumulate
# across repeated calls in the same shell session.
cmd /c "set JAVA_TOOL_OPTIONS=$agentOpts && $Command"
```

## 3. Configuration
Ensure you have the following environment variables set (obtained from `setup_project`):
- `API_KEY`
- `APP_NAME`
- `PROJECT_ID`

## 4. Usage
Prefix any Java-related command with the wrapper script to enable instrumentation.

### Linux / macOS / WSL (`.sh`)
Arguments are passed directly — no quoting needed.

- Maven (Specific test): `./scripts/run_java_with_agent.sh mvn test -Dtest=MyTestClass`
- Gradle (Specific test): `./scripts/run_java_with_agent.sh ./gradlew test --tests MyTestClass`
- Ant (Specific test): `./scripts/run_java_with_agent.sh ant test -Dtestcase=MyTestClass` (Note: target may vary, e.g., `ant test-single`)
- Direct Java: `./scripts/run_java_with_agent.sh java -jar target/app.jar`

### Windows PowerShell (`.ps1`)
> [!IMPORTANT]
> The **entire command must be passed as a single quoted string**. PowerShell treats `-D` flags containing dots (e.g., `-Djacoco.skip=true`) as variable expressions when they appear as separate arguments, which causes a parse error. Wrapping the whole command in quotes avoids this.

- Maven (Specific test): `./scripts/run_java_with_agent.ps1 "mvn test -Dtest=MyTestClass"`
- Gradle (Specific test): `./scripts/run_java_with_agent.ps1 "./gradlew test --tests MyTestClass"`
- Ant (Specific test): `./scripts/run_java_with_agent.ps1 "ant test -Dtestcase=MyTestClass"`
- Direct Java: `./scripts/run_java_with_agent.ps1 "java -jar target/app.jar"`

> [!IMPORTANT]
> **Never run the full test suite** (e.g., `mvn test` without `-Dtest`) with the agent. This is extremely inefficient for debugging and can produce overwhelming trace data. Always target the specific test related to the issue.


## 5. Verification
Run a simple command like `./scripts/run_java_with_agent.sh java -version` (Linux/macOS) or `./scripts/run_java_with_agent.ps1 "java -version"` (Windows). You should see `Downloading Agent...` if it's the first time.
Check the console output for any agent initialization messages.
