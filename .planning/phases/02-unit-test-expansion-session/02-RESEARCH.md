# Phase 2: Unit Test Expansion (Session) - Research

## Mocking Firebase Admin Auth

O `firebase_admin.auth` lança exceções específicas que precisam ser mockadas para testar o tratamento de erros em `models/session.py`.

### Exceções Alvo
- `auth.InvalidIdTokenError`
- `auth.ExpiredIdTokenError`
- `auth.RevokedIdTokenError`
- `exceptions.FirebaseError` (para erros genéricos de serviço)

### Estratégia de Mock
Usar `unittest.mock.patch` no local onde o `auth` é utilizado (ex: `@patch('models.session.auth.create_session_cookie')`).

```python
from firebase_admin import auth, exceptions

# Simulando erro de token revogado
mock_create.side_effect = auth.RevokedIdTokenError("Token revoked")
```

## Testing Cookie Security Flags (Integration)

Para validar `httponly=True` e `secure` baseados no ambiente, utilizaremos o `test_client` do Flask.

### Verificação de Headers
O header `Set-Cookie` contém as flags separadas por ponto e vírgula.

```python
def test_session_cookie_flags(client):
    response = client.post('/api/v1/sessions', json=data)
    cookie_header = response.headers.get('Set-Cookie')
    assert 'HttpOnly' in cookie_header
    # Para testar 'Secure', precisaremos mockar o ENVIRONMENT no endpoint
```

### Mocking ENVIRONMENT
Como o endpoint `api/v1/sessions.py` usa `os.getenv("ENVIRONMENT")`, podemos patchear isso nos testes para simular produção:

```python
@patch('api.v1.sessions.os.getenv')
def test_secure_cookie_in_production(mock_getenv, client):
    mock_getenv.return_value = "production"
    response = client.post('/api/v1/sessions', json=data)
    assert 'Secure' in response.headers.get('Set-Cookie')
```

## Cobertura (Nyquist Strategy)
Para atingir >90% em `models/session.py`:
1. **Success Cases:** `create` e `verify_cookie` com mocks retornando valores válidos.
2. **Error Cases (create):** `InvalidIdTokenError`, `ExpiredIdTokenError`, `RevokedIdTokenError`, `ValueError`, `FirebaseError`.
3. **Error Cases (verify_cookie):** `ExpiredSessionCookieError`, `RevokedSessionCookieError`, `InvalidSessionCookieError`, `CertificateFetchError`, `Exception` genérica.
4. **Input Validation:** Tokens/cookies vazios, durações inválidas.
