# Phase 2: Unit Test Expansion (Session) - Context

## Decisões de Implementação

### 1. Testes de Integração para Cookie Flags
- **Decisão:** Validar as flags `HttpOnly` e `Secure` através de testes de integração da API (`api/v1/sessions.py`) em vez de testes unitários do model.
- **Racional:** Essas flags são configuradas no objeto `Response` do Flask no endpoint, e não no model. Testes de integração garantem que o contrato de segurança da API está sendo cumprido na ponta.

### 2. Mocking de Firebase Admin
- **Decisão:** Seguir o padrão de mocking usado na Fase 1 (Gemini), utilizando `unittest.mock.patch` e `side_effect` para simular exceções do SDK.
- **Racional:** Consistência entre as suítes de teste e facilidade de manutenção.

### 3. Simulação de Ambiente (Secure Flag)
- **Decisão:** Patchear `os.getenv` nos testes de integração para alternar entre `development` e `production` e validar a presença/ausência da flag `Secure`.

## Restrições
- Não realizar chamadas reais ao Firebase.
- Manter compatibilidade com `pytest`.
