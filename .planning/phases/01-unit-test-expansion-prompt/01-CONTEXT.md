# Phase 1: Unit Test Expansion (Prompt) - Context

**Gathered:** 2026-04-26
**Status:** Ready for planning

<domain>
## Phase Boundary
Esta fase foca exclusivamente na criação de uma suíte completa de testes unitários para o arquivo `models/prompt.py`, visando aumentar a cobertura de 54% para >95%.

O objetivo é garantir que todas as funções de validação interna (`validate_topic`, `validate_days`, `validate_knowledge`, `validate_focus_time`) e as funções de orquestração (`make`, `process`, `format`) funcionem corretamente para todos os tipos de entrada.

</domain>

<decisions>
## Implementation Decisions

### Testing Strategy
- **Mocks vs VCR:** Para a função `validate_relevance`, utilizaremos **Mock puro** da biblioteca `unittest.mock` para simular as respostas do `genai.Client`. Não faremos chamadas reais ao Gemini nem usaremos VCR nesta fase unitária.
- **Exhaustive Testing:** Implementar testes exaustivos para cada cenário possível utilizando `pytest.mark.parametrize`. Isso inclui:
  - Limites de caracteres (exato, um abaixo, um acima).
  - Tipos de dados inválidos (passar int onde espera str e vice-versa).
  - Casos de sucesso e falha para cada função individualmente.
- **Structure:** Criar o arquivo em `tests/unit/models/test_prompt.py`, seguindo o padrão de nomenclatura e asserções já existente no projeto.
- **Assertions:** Validar não apenas a ocorrência da exceção, mas também o conteúdo da mensagem e da ação retornada pelo `ValidationError.toDict()`.

### locked_requirements
- A cobertura de `models/prompt.py` deve ser verificada e confirmada como superior a 95%.
- Nenhuma chamada de rede real deve ocorrer durante a execução destes testes.

</decisions>

<canonical_refs>
## Canonical References
- `models/prompt.py` — Arquivo alvo da refatoração.
- `tests/unit/models/test_guide.py` — Referência de padrão de testes unitários.
- `errors.py` — Definições de `ValidationError` e `ServiceError`.

</canonical_refs>

<specifics>
## Specific Ideas
- Simular falhas de cota (429) e erros de servidor (503) no mock do `genai.Client` para testar a lógica de retry em `validate_relevance`.
- Testar a função `process` para garantir que o stripping de espaços funciona em diferentes tipos de entrada.
- Testar a função `format` para garantir que o XML gerado está correto.

</specifics>

<deferred>
## Deferred Ideas
- Refatoração da lógica de prompts para arquivos externos (será tratada na Fase 4).
- Aumento de cobertura para `models/session.py` (será tratada na Fase 2).

</deferred>

---
*Phase: 01-unit-test-expansion-prompt*
*Context gathered: 2026-04-26*
