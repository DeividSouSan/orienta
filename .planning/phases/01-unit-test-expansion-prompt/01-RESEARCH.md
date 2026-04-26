# Phase 1: Unit Test Expansion (Prompt) - Research

## Findings

### 1. Mocking google-genai
- **Client Mock:** `patch('google.genai.Client')` is sufficient.
- **Retry Logic:** To test `validate_relevance`'s retry loop, use `side_effect` on the mock's `models.generate_content` method.
- **Response Structure:** The response object should have a `.parsed` attribute containing an instance of `ValidationResult` (Pydantic model).

### 2. Pytest Patterns
- **Parametrization:** Use `pytest.mark.parametrize` with `ids` for readability.
- **Exception Checks:** `with pytest.raises(ValidationError) as exc:` followed by `assert exc.value.toDict() == expected`.

### 3. Coverage Analysis
- Current coverage of `models/prompt.py`: 54%.
- Missing areas: Individual validation functions, internal helper calls, error handling branches in `validate_relevance`.

## Dependencies
- `pytest`
- `pytest-cov`
- `unittest.mock` (standard library)
- `faker` (already in dev dependencies)
