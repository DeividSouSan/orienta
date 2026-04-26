# Requirements: Refactoring & Stability

Este documento detalha os requisitos técnicos para a fase atual de manutenção e estabilização do Orienta.

## User Persona: Desenvolvedor (Manutenção)
Como desenvolvedor do projeto, quero uma base de código robusta e testada para que eu possa evoluir o sistema sem introduzir regressões ou instabilidades.

---

## 1. Cobertura de Testes e Qualidade

### 1.1 Cobertura de Unidade (Prompt Model)
- **Status:** Pendente
- **Descrição:** O arquivo `models/prompt.py` deve possuir testes unitários para todas as funções de validação interna (`validate_topic`, `validate_days`, etc).
- **Critério de Aceite:** Coverage de `models/prompt.py` deve subir de 54% para >95%.

### 1.2 Cobertura de Sessão (Session Model)
- **Status:** Pendente
- **Descrição:** Testar diretamente os métodos `create()` e `verify_cookie()` do `models/session.py`, mockando o Firebase.
- **Critério de Aceite:** Coverage de `models/session.py` deve subir de 45% para >90%.

---

## 2. Arquitetura e Resiliência

### 2.1 Centralização de Erros
- **Status:** Parcial
- **Descrição:** Todos os erros de comunicação com APIs externas (Firebase/Gemini) devem ser capturados e transformados em exceções customizadas do `errors.py`.
- **Critério de Aceite:** Nenhuma exceção bruta de `requests` ou `google-genai` deve vazar para a camada de API.

### 2.2 Desacoplamento de Prompts
- **Status:** Em andamento
- **Descrição:** A lógica de construção de prompts deve ser isolada de forma que mudanças nos templates markdown não quebrem a lógica do modelo.
- **Critério de Aceite:** Testes unitários de prompt devem validar a estrutura final do prompt gerado.

---

## 3. Performance de Testes

### 3.1 Estabilidade dos Cassetes VCR
- **Status:** Em andamento
- **Descrição:** Garantir que a troca de modelos no `.env` não invalide todos os cassetes ou que o processo de regravação seja automatizado/documentado.
- **Critério de Aceite:** Suite de testes deve rodar em < 25s localmente (usando VCR).

---

## Tabela de Prioridades

| ID | Requisito | Impacto | Esforço | Prioridade |
|---|---|---|---|---|
| 1.1 | Unit Tests (Prompt) | Alto | Baixo | **P0** |
| 1.2 | Unit Tests (Session) | Médio | Médio | **P1** |
| 2.1 | Global Error Handling | Alto | Médio | **P1** |
| 2.2 | Prompt Decoupling | Médio | Médio | **P2** |
