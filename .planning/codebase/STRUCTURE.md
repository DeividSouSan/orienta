# Project Structure

## Directories

- **`api/v1/`**: Flask routes and blueprints.
- **`dtos/`**: Pydantic schemas for API requests/responses.
- **`frontend/`**: React application (located in `frontend/orienta-react`).
- **`infra/`**: Infrastructure configuration (Firestore rules, etc.).
- **`models/`**: Core logic and database interaction (Auth, Guide, Prompt, Session, User).
- **`objects/`**: Domain Value Objects (DDD approach).
- **`prompts/`**: Markdown files with templates for LLM prompts.
- **`tests/`**:
  - `integration/`: Tests exercising multiple layers and external APIs (recorded via VCR).
  - `unit/`: Isolated tests for logic and Value Objects.
- **`utils.py`**: Shared utility functions and app initialization.
- **`main.py`**: Flask application entry point.

## Key Files
- `pyproject.toml`: Backend dependencies and tool configurations.
- `service-account.json`: Firebase credentials.
- `.env`: Environment variables.
