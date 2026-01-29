# Syncause Node.js SDK Installation Guide

When tasked with installing the TS/JS Probe into a project, follow this prioritized execution flow:

## 1. Automated Installation
Identify the project type (Next.js, TypeScript, or JavaScript) and run the installer directly from GitHub:
```bash
curl -sL https://raw.githubusercontent.com/Syncause/ts-agent-file/v1.6.0/install_probe.sh | bash
```
*Note: For Next.js projects, the script downloads `instrumentation.node.next.ts` from GitHub (default `v1.3.0`) and renames it to `instrumentation.node.ts`.*

### Replace apikey and appName in instrumentation.node.ts / instrumentation.node.js

apikey: {apiKey}
appName: {appName}
projectId: {projectId}

Replace the following:

```
const API_KEY = 'your-api-key-here'
const APP_NAME = 'your-app-name-here'
const PROJECT_ID = 'your-project-id-here'  // This is your project ID
```

## 2. Next.js Specific Configuration (CRITICAL)
If the project is **Next.js**, the script downloads the files but you **MUST** manually update `src/instrumentation.ts`.

### Step 2.1: Update `src/instrumentation.ts`
For Next.js 15+, use the official `register` function and include a runtime check to ensure instrumentation only runs in the Node.js environment.

```typescript
export async function register() {
    if (process.env.NEXT_RUNTIME === 'nodejs') {
        const { init } = await import('./instrumentation.node');
        init();
    }
}
```

### Step 2.2: Generate Installation Patch
After completing the installation and configuration, you must generate a clean patch of all changes made to the project and save it in the `.syncause/installation.patch` file.

**IMPORTANT**:
1. Use your internal knowledge of the specific edits you made to generate this patch.
2. **DO NOT** use `git diff` as it might include unrelated changes.
3. **DO NOT** include any log files or temporary files in the patch.
4. Ensure the patch is in the standard unified diff format.

## 3. Verification
Verify the installation was successful:
- **Environment**: Try running `npm run dev`.
- **Logs**: Look for:
  - `[next.config] probe-loader enabled`
  - `[DEBUG] OpenTelemetry SDK started`
  - `[DEBUG] Connected to proxy server` (if logs are enabled)
- **API Check**: Run `curl http://localhost:43210/remote-debug/spans/stats`. It should return JSON data with `totalSpans > 0` after visiting the app.

## 4. Manual Fallback & Troubleshooting
If the script fails or the app doesn't start:
1.  **Dependencies**: Manually install `@opentelemetry/sdk-node @opentelemetry/api @opentelemetry/auto-instrumentations-node @opentelemetry/sdk-metrics @opentelemetry/sdk-trace-node @opentelemetry/core express ws`.
2.  **TS Project**: Ensure `tsx --import ./src/instrumentation.node.ts` is in the `dev` script.
3.  **Conflict**: If "Ready in XXXms" shows but no data, ensure `instrumentation.ts` exists in the `src` folder for Next.js and has the `register()` function.

**Goal**: Confirm the probe is active by verifying the HTTP stats endpoint.