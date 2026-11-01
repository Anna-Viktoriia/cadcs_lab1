# Repository instructions

## Build, test, and lint

The application files and build scripts are created by the `/lab1-init`
workflow; they may not exist before that workflow has completed.

- Run the cross-platform CI script from the repository root:
  - Linux/macOS: `./ci.sh`
  - Windows: `ci.bat`
- Run the complete test suite directly:
  - Linux/macOS: `.venv/bin/python -m pytest`
  - Windows: `.venv\Scripts\python.exe -m pytest`
- Run the single addition test:
  - Linux/macOS: `.venv/bin/python -m pytest -v tests/test_calc.py::test_basic_addition`
  - Windows: `.venv\Scripts\python.exe -m pytest -v tests/test_calc.py::test_basic_addition`
- Package the application through `ci.sh` or `ci.bat`; those scripts also run
  the tests and place the PyInstaller output in `dist/`.
- No lint command is configured in the repository.

Run Python dependencies only through the project virtual environment. The CI
scripts use the environment's interpreter directly and do not need activation.

## Architecture and agent workflow

This repository defines a Copilot agent workflow for generating and validating
a small cross-platform Python `hello` package:

1. Select the **Build Engineer** custom agent in Copilot Chat.
2. Run `/lab1-init`.
3. The orchestrator reads and follows the stage instructions in order:
   `git-init` → `create-project` → `create-build` → `create-actions` → `check`.
4. Each creation stage uses its matching skill in `.github/skills/`.
   The workflow creates the `src/hello` package, pytest coverage, virtual
   environment scripts, and a GitHub Actions matrix workflow. `check` validates
   the results.

The custom agent is the role and tool boundary; prompt files are user-invocable
commands; skills contain the detailed, reusable procedures. Keep these layers
aligned when changing the workflow. See [docs/architecture.md](../docs/architecture.md)
for the component relationships and [docs/usage.md](../docs/usage.md) for run
instructions.

## Repository-specific conventions

- Python source is under `src/hello`; `hello.calc.add` is the tested function,
  and `python -m hello` prints `Hello, World!`.
- `pytest` must resolve the package from `src` through `pytest.ini` or the
  existing `pyproject.toml` configuration.
- Keep dependency installation, tests, and PyInstaller packaging in
  `ci.sh`/`ci.bat`. GitHub Actions should only set up Python, call the
  platform script, and upload `dist/`.
- Create files only after checking whether they exist. Preserve existing
  content, make repeat runs idempotent, and avoid duplicate requirements or
  `.gitignore` entries.
- Keep `.venv/`, `build/`, `dist/`, Python bytecode, and test caches out of Git.
- The orchestrator is sequential: stop on the first failed prerequisite,
  stage, or check; report the actual failure and mark later stages as not run.
