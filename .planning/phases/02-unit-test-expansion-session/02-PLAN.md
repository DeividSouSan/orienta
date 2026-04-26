# Phase 2: Unit Test Expansion (Session) - Plan

## Wave 1: Unit Tests (Basic Flows)

### Task 1.1: Setup Test File & Success Cases
- **Action:** Criar `tests/unit/models/test_session.py`. Implementar testes de sucesso para `create` e `verify_cookie`.
- **Read First:** `models/session.py`.
- **Acceptance Criteria:** `create` retorna um cookie (mocked) e `verify_cookie` retorna o payload (mocked).

### Task 1.2: Test Input Validations
- **Action:** Testar tokens vazios, cookies vazios e durações excedendo o limite de 14 dias.
- **Acceptance Criteria:** Lança `ValidationError` com as mensagens corretas.

## Wave 2: Unit Tests (Firebase Errors)

### Task 2.1: Test `create` Error Handling
- **Action:** Mockar `auth.create_session_cookie` para lançar `InvalidIdTokenError`, `ExpiredIdTokenError`, `RevokedIdTokenError` e `FirebaseError`.
- **Acceptance Criteria:** Mapeia corretamente para `UnauthorizedError` ou `ServiceError`.

### Task 2.2: Test `verify_cookie` Error Handling
- **Action:** Mockar `auth.verify_session_cookie` para lançar `ExpiredSessionCookieError`, `InvalidSessionCookieError`, `CertificateFetchError`.
- **Acceptance Criteria:** Mapeia corretamente para `UnauthorizedError` ou `ServiceError`.

## Wave 3: Integration Tests (API & Cookies)

### Task 3.1: Integration Test for Session Creation
- **Action:** Criar/Atualizar testes de integração para `POST /api/v1/sessions`. Validar o header `Set-Cookie`.
- **Acceptance Criteria:** Verifica se `HttpOnly` está sempre presente e `Secure` depende do `ENVIRONMENT`.

### Task 3.2: Final Coverage Audit
- **Action:** Executar `uv run pytest --cov=models/session.py tests/unit/models/test_session.py`.
- **Acceptance Criteria:** Cobertura > 90%.

---

## Verification
- **Test Command:** `uv run pytest tests/unit/models/test_session.py`
- **Goal:** Estabilidade total na gestão de sessões.
