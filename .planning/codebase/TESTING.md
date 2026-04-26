# Testing Strategy

## Tools
- **Test Runner:** `pytest`
- **Coverage:** `pytest-cov`
- **Recording:** `vcrpy` (via `pytest-recording`)

## Organization
- **Unit Tests (`tests/unit/`):** Test isolated logic, DTOs, and Value Objects. No network calls.
- **Integration Tests (`tests/integration/`):** Test full flows from API to Database/IA.
- **Cassettes:** Recorded in `cassettes/` directories using VCR to avoid repetitive network costs and rate limits.

## Performance Otimization
- Shared users (module/session scope) to reduce Firebase Auth calls.
- Removed artificial delays in cleanup fixtures.
- VCR ignores localhost and common Google auth endpoints to stay stable.

## Coverage State
- **Current Coverage:** ~86%
- **Targets for improvement:** `models/prompt.py` and `models/session.py`.
