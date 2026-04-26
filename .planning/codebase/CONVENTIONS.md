# Coding Conventions

## Backend
- **Type Hinting:** Required for all function signatures.
- **DTOs:** Mandatory for data entering/leaving the API layer.
- **Value Objects:** Used for business rule validation in the domain.
- **Error Handling:** Centralized custom exceptions in `errors.py`.
- **Imports:** Sorted with `isort`.
- **Linting/Formatting:** [Ruff](https://beta.ruff.rs/) is used with pre-commit hooks.

## Git & Workflow
- **Commit Messages:** [Conventional Commits](https://www.conventionalcommits.org/) required (checked by commitizen).
- **Branching:** Work primarily done in `development` branch.
- **Pre-commit:** Hooks for whitespace, end-of-file, YAML check, Ruff, and isort.

## Documentation
- Use markdown artifacts for reports.
- Detailed docstrings for complex logic.
