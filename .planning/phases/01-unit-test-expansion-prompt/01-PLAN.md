# Phase 1: Unit Test Expansion (Prompt) - Plan

Este plano detalha a criação de testes unitários exaustivos para `models/prompt.py`, garantindo alta cobertura e estabilidade sem dependência de rede.

## Wave 1: Setup & Data Validation (Sequential)

### Task 1.1: Setup Test File & Basic Mocks
- **Action:** Criar o arquivo `tests/unit/models/test_prompt.py` com os imports necessários (`pytest`, `unittest.mock`, `models.prompt`).
- **Read First:** `models/prompt.py`, `tests/unit/models/test_guide.py`.
- **Acceptance Criteria:** `tests/unit/models/test_prompt.py` existe e importa `prompt` sem erros.

### Task 1.2: Test `process` and `format` Functions
- **Action:** Implementar testes para a limpeza de strings em `process` e a formatação XML em `format`.
- **Read First:** `models/prompt.py`.
- **Acceptance Criteria:** Testes validam o `strip()` em todos os campos do dicionário e a estrutura XML resultante.

### Task 1.3: Test Standalone Validations (Topic, Knowledge, Focus, Days)
- **Action:** Implementar baterias exaustivas usando `pytest.mark.parametrize` para `validate_topic`, `validate_knowledge`, `validate_focus_time` e `validate_days`.
- **Read First:** `models/prompt.py`.
- **Acceptance Criteria:** Cobertura de sucesso e falha (limites e tipos) para cada função. Mensagens de erro conferem com `prompt.py`.

## Wave 2: AI Orchestration (Sequential)

### Task 2.1: Mock Gemini for `validate_relevance`
- **Action:** Implementar o mock do `genai.Client` em `test_prompt.py`. Simular o retorno do objeto `ValidationResult` parseado.
- **Read First:** `models/prompt.py`, `01-RESEARCH.md`.
- **Acceptance Criteria:** Testes validam cenários onde `is_valid` é True e False sem fazer chamadas de rede.

### Task 2.2: Test Retry Logic & Errors in `validate_relevance`
- **Action:** Simular exceções `ClientError` (429) e `ServerError` (503) para garantir que o loop de `VALIDATION_MODELS` funciona conforme esperado.
- **Read First:** `models/prompt.py`.
- **Acceptance Criteria:** O código deve tentar o próximo modelo em caso de erro 429/503 e levantar `ServiceError` se todos falharem.

### Task 2.3: Test Orchestrator Function `make`
- **Action:** Testar a função principal `make`, garantindo que ela chama corretamente o processamento e as validações.
- **Read First:** `models/prompt.py`.
- **Acceptance Criteria:** `make` retorna a string formatada em caso de sucesso e propaga exceções de validação em caso de falha.

## Wave 3: Verification (Sequential)

### Task 3.1: Final Coverage Audit
- **Action:** Executar a suíte de testes com relatório de cobertura focado no arquivo alvo.
- **Command:** `uv run pytest --cov=models/prompt.py tests/unit/models/test_prompt.py`
- **Acceptance Criteria:** Relatório indica coverage >= 95%.

---

## Verification
- **Test Command:** `uv run pytest tests/unit/models/test_prompt.py`
- **Acceptance Criteria:** Todos os testes unitários (estimados em 25+) devem passar de forma determinística.
