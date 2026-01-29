# Syncause Python SDK Installation Guide

<step_1>

### Add `syncause_tracer` as a Project Dependency

Your task is to **identify the project's dependency management system** and add `syncause_tracer` as a dependency in a **safe, idempotent, and non-destructive way**.

Do NOT modify lock files unless explicitly instructed.

---

### 1. Identify the Dependency File (Priority Order)

Detect the dependency system in the following order:

1. `pyproject.toml`
   - `[tool.poetry.dependencies]` → Poetry
   - `[project.dependencies]` → PEP 621 (pip / uv / pdm)
2. `requirements.txt`
3. `setup.py` / `setup.cfg` (legacy, fallback only)

If multiple systems exist:
- Prefer `pyproject.toml`
- Do NOT add the dependency to more than one file

---

### 2. Add Dependency Based on the Detected System

#### A. Using `requirements.txt`

Append the following line **if it does not already exist** and install the dependency:

```text
https://github.com/Syncause/syncause-sdk/releases/download/syncause_tracer_v0.2.7/syncause_tracer-0.2.7-py3-none-any.whl
```

Rules:
- Avoid duplicate entries
- Preserve file formatting and comments
- Do NOT reorder existing dependencies

---

#### B. Using `pyproject.toml` (Poetry)

Add the dependency under `[tool.poetry.dependencies]` and install the dependency:

```toml
[tool.poetry.dependencies]
syncause_tracer = { url = "https://github.com/Syncause/syncause-sdk/releases/download/syncause_tracer_v0.2.7/syncause_tracer-0.2.7-py3-none-any.whl" }
```

Rules:
- Do NOT remove or modify existing dependencies
- Do NOT add a duplicate if it already exists
- Do NOT update `poetry.lock`

---

#### C. Using `pyproject.toml` (PEP 621: pip / uv / pdm)

Add the dependency under `[project.dependencies]` and install the dependency:

```toml
[project]
dependencies = [
  "syncause_tracer @ https://github.com/Syncause/syncause-sdk/releases/download/syncause_tracer_v0.2.7/syncause_tracer-0.2.7-py3-none-any.whl"
]
```

Rules:
- Preserve existing dependency order
- Ensure valid TOML syntax
- Do NOT touch lock files (e.g. `pdm.lock`, `uv.lock`)

---

### 3. Validation Rules

Before applying changes:
- Confirm the dependency is not already present
- Ensure the file is writable
- Ensure no syntax errors are introduced

After applying changes:
- Only the selected dependency file should be modified

If no supported dependency file is found:
- Report that manual installation is required
- Do NOT create new dependency files

</step_1>


<step_2>
### Locate the Project Entry Point

Your task is to **identify the correct project entry file** where
application-level initialization code should be executed **exactly once
at startup**.

Do NOT guess. Follow the rules below in order.

------------------------------------------------------------------------

### 1. Definition of "Entry Point"

The entry point is the Python file that: - Is executed when the
application starts - Creates or launches the web application - Runs
before request handling begins - Is suitable for global initialization
code

Only need one entry point. 

------------------------------------------------------------------------

### 2. Framework-Specific Identification Rules (Priority Order)

#### Django

Identify the entry point in the following order: 1. `manage.py` (for
development / CLI startup) 2. `project/wsgi.py` (WSGI deployment) 3.
`project/asgi.py` (ASGI deployment)

------------------------------------------------------------------------

#### FastAPI

Identify the file that: - Creates a `FastAPI()` instance - Is referenced
by `uvicorn` (e.g. `uvicorn main:app`)

Common filenames: - `main.py` - `app.py`

Typical patterns:

``` python
app = FastAPI()
```

or 

``` python
def create_app():
    app = Flask(__name__)
    return app
```

------------------------------------------------------------------------

#### Flask

Identify the file that: - Creates a `Flask(__name__)` application - Or
uses an application factory (`create_app()`)

Common patterns:

``` python
app = Flask(__name__)
```

------------------------------------------------------------------------

### 3. Generic Python Projects (Fallback)

If no known framework is detected:
1. Look for:
    - `main.py`
    - `app.py`
    - A file referenced by `__main__`
2. Prefer files containing:
    - `if __name__ == "__main__":`
    - A `main()` function that starts the program
3. **Location Priority**:
    - **Prefer scripts located at the project root** over those in subdirectories.
    - Select the "most top-level" entry script available.

------------------------------------------------------------------------

### 4. Validation Rules

Before selecting a file: - Ensure it is executed only once at startup -
Ensure it is NOT: - A settings/config-only file - A model, router, or utility module - Imported repeatedly by other modules

If multiple candidates exist: - Choose the one most directly responsible
</step_2>

<step_3>
Action: Inject Initialization Code

Insert the following initialization code at the top of the identified entry file.

Placement Logic: To prevent syntax errors, you must determine the correct insertion point by following these priority rules:
    Scan for Headers: Skip past any Shebang (#!) or Encoding lines (# -*- ...).
    Scan for Metadata: Skip past any Module Docstrings ("""...""") or Copyright/License comment blocks.
    Scan for Future Imports: Skip past any from __future__ imports.
    INSERT HERE: Place the code immediately after the above elements.
    Before Standard Imports: Ensure the code is placed before any standard library or third-party imports (e.g., import os).

Code to Insert:

``` python
from syncause_tracer import initialize
initialize(
    api_key="{apiKey}",
    app_name="{appName}",
    project_id="{projectId}"
)
```
</step_3>