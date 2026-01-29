# Syncause Python SDK Uninstallation Guide
<step_1>
### 1. Remove Initialization Code (Important)

Before uninstalling the package, you **must** remove the SDK integration code from your project to prevent runtime errors.

**Action**: Search for and delete the following code snippet from your project:

```python
from syncause_tracer import initialize
initialize(
    api_key="...",
    app_name="...",
    project_id="..."
)
```

**How to locate it**: Use code search to find files containing `from syncause_tracer import initialize`. This code is typically located in your application's entry point (e.g., `main.py`, `app.py`, `manage.py`, `wsgi.py`, or `asgi.py`).
</step_1>

<step_2>
### 2. Uninstall syncause_tracer

**Action**: Remove `syncause_tracer` from your project's dependency files.

1. **Search for the dependency**: Look for `syncause_tracer` in your dependency files. It may appear as:
   - A GitHub release URL (e.g., `https://github.com/Syncause/syncause-sdk/releases/download/syncause_tracer_v0.2.7/syncause_tracer-0.2.7-py3-none-any.whl`)
   - A package name: `syncause_tracer`

2. **Remove the line** from the appropriate file:
   - `requirements.txt` - Delete the line containing `syncause_tracer`
   - `pyproject.toml` - Delete the line containing `syncause_tracer` from within the `[project.dependencies]` or `[tool.poetry.dependencies]` section

3. **Run the uninstall command** based on your dependency manager:
   ```bash
   # pip
   pip uninstall syncause_tracer
   
   # Poetry (automatically updates pyproject.toml)
   poetry remove syncause_tracer
   
   # uv
   uv sync
   
   # pdm
   pdm sync
   ```
</step_2>

<step_3>
**Verify Uninstallation**
Restart your service. Ensure the application runs normally without the Syncause tracer.
</step_3>

<important>
- If you forget to remove the `import` statements in Step 1, your application will fail to start.
</important>