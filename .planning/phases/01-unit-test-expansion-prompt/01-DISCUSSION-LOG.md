# Phase 1: Unit Test Expansion (Prompt) - Discussion Log

## Areas Discussed

### 1. Estratégia de Mocking para IA
- **Opções apresentadas:** Mock puro vs VCR.
- **Decisão:** Mock puro.
- **Racional:** O comportamento de `is_valid` é simples e não determinístico, não justificando o custo/complexidade de uma chamada real ao Gemini para testes unitários.

### 2. Rigor dos Testes
- **Opções apresentadas:** Testes básicos vs Testes exaustivos.
- **Decisão:** Testes exaustivos.
- **Racional:** Garantir que todos os limites e tipos de entrada sejam validados com `pytest.mark.parametrize`.

### 3. Padrão de Organização
- **Decisão:** Seguir o padrão atual do projeto (`tests/unit/models/test_prompt.py`).
- **Racional:** Manter consistência com a estrutura existente.

## Deferred Ideas
- Refatoração profunda da arquitetura de IA (adiado para Fase 4).
