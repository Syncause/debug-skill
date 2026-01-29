# Syncause Node.js SDK Uninstallation Guide

To remove the Syncause SDK from your project, follow these steps to clean up files and dependencies.

## 1. Remove Instrumentation Files

### Generic Node.js

Delete `instrumentation.ts`


### Generic Node.js / TypeScript Projects
Delete the instrumentation file created during installation:

- **TypeScript**: Delete `instrumentation.node.ts`
- **JavaScript**: Delete `instrumentation.node.js`

### Next.js Projects
1. **Delete the helper file**: Remove `instrumentation.node.ts` (or `instrumentation.node.js` if you compiled it).
2. **Revert `src/instrumentation.ts`**:
   - Open `src/instrumentation.ts` (or `instrumentation.ts` in root).
   - Remove the `register` function or the code block importing `./instrumentation.node`.
   - If the file is now empty (and wasn't used for anything else), you can safely delete it.

## 2. Clean Up Dependencies

Uninstall the OpenTelemetry packages and libraries added by the installer.

Run the following command:

```bash
npm uninstall @opentelemetry/sdk-node @opentelemetry/api @opentelemetry/auto-instrumentations-node @opentelemetry/sdk-metrics @opentelemetry/sdk-trace-node @opentelemetry/core
```
*(Use `yarn remove` or `pnpm remove` if applicable)*

## 3. Configuration & Verification

1. **Check `package.json`**:
   - If you manually added `--import ./instrumentation.node.ts` (or similar) to your `dev` or `start` scripts, **remove it**.

2. **Verify Removal**:
   - Run your application (e.g., `npm run dev`).
   - Check the logs. You should **NOT** see messages like `[DEBUG] OpenTelemetry SDK started` or `[next.config] probe-loader enabled`.
   - The application should function normally.
