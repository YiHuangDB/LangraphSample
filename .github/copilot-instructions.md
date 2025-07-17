# Copilot Instructions for LangraphSample

## Project Overview
This is a minimal Python project. The main entry point is `main.py` at the workspace root. There are currently no additional modules, configuration files, or documentation present.

## Architecture & Data Flow
- **Single-file structure:** All logic resides in `main.py`. There are no submodules or external service boundaries.
- **No external dependencies:** The project does not use any third-party packages or frameworks by default. If you add dependencies, document them in a `requirements.txt` file and update this guide.

## Developer Workflows
- **Run the project:**
  ```powershell
  python main.py
  ```
- **Add dependencies:**
  - Create a `requirements.txt` file if you introduce external packages.
  - Install with:
    ```powershell
    pip install -r requirements.txt
    ```
- **Testing:**
  - No test framework is present. If you add tests, place them in a `tests/` directory and update this guide.

## Conventions & Patterns
- **Code organization:**
  - Keep all logic in `main.py` unless the project grows.
  - Use clear function and variable names; add docstrings for any non-trivial logic.
- **Extending the project:**
  - For new features, consider splitting code into modules as the project grows.
  - Update this file to reflect new architectural decisions.

## Integration Points
- **External APIs:** None currently integrated.
- **Cross-component communication:** Not applicable in the current structure.

## Examples
- To add a function:
  ```python
  def greet(name: str) -> str:
      """Return a greeting for the given name."""
      return f"Hello, {name}!"
  ```
- To run the script:
  ```powershell
  python main.py
  ```

---
**Update this file as the project evolves.**
