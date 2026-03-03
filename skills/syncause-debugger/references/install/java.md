# Syncause Java Agent Installation Guide

When tasked with installing the Java Agent into a project, follow this prioritized execution flow:

## 1. Identify Project Type
Detect if the project is using Maven (`pom.xml`), Gradle (`build.gradle` or `build.gradle.kts`), or Ant (`build.xml`).

## 2. Create Wrapper Scripts
To avoid manual configuration of `JAVA_TOOL_OPTIONS`, you MUST create wrapper scripts in the `scripts/` directory of the project root.

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
export JAVA_TOOL_OPTIONS=$(echo "$JAVA_TOOL_OPTIONS $AGENT_OPTS" | xargs)

# Execute the remaining command
exec "$@"
```

### Step 2.2: Create `scripts/run_java_with_agent.ps1` (for Windows PowerShell)

```powershell
param(
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$Command
)

# Description: Wrapper to run any command with the Syncause Agent loaded via JAVA_TOOL_OPTIONS locally.

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

# Set local environment and execute
$agentOpts = "-javaagent:$agentJar=api_key=$env:API_KEY,project_name=$env:APP_NAME,project_id=$env:PROJECT_ID"
$env:JAVA_TOOL_OPTIONS = "$($env:JAVA_TOOL_OPTIONS) $agentOpts".Trim()

# Run the command with arguments
& @Command
```

## 3. Configuration
Ensure you have the following environment variables set (obtained from `setup_project`):
- `API_KEY`
- `APP_NAME`
- `PROJECT_ID`

## 4. Usage
Prefix any Java-related command with the wrapper script to enable instrumentation.

**Examples:**
- Maven (Specific test): `./scripts/run_java_with_agent.sh mvn test -Dtest=MyTestClass`
- Maven (All tests): `./scripts/run_java_with_agent.sh mvn test`
- Gradle (Specific test): `./scripts/run_java_with_agent.sh ./gradlew test --tests MyTestClass`
- Ant: `./scripts/run_java_with_agent.sh ant test` (or specific target: `./scripts/run_java_with_agent.sh ant test-single -Dtestcase=MyTestClass`)
- Direct Java: `./scripts/run_java_with_agent.sh java -jar target/app.jar`


## 5. Verification
Run a simple command like `./scripts/run_java_with_agent.sh java -version`. You should see `Downloading Agent...` if it's the first time.
Check the console output for any agent initialization messages.
