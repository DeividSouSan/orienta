# Roadmap: Orienta Stability & Refactoring

Foco: Melhoria da cobertura de testes, tratamento de erros e desacoplamento arquitetural.

## Milestone 1: Technical Excellence (Q2 2026)

- [x] **Fase 1: Expansão de Testes Unitários (Prompt)** — ✅ Concluído
- **Task 1.1:** Criar suíte de testes unitários para `models/prompt.py`. — ✅
- **Task 1.2:** Validar funções de parseamento de tópicos e dias. — ✅
- **Task 1.3:** Validar funções de formatação de mensagens para o Gemini. — ✅
- **UAT:** Coverage de `models/prompt.py` > 95%. (Atingido: 97%)

- [x] **Fase 2: Expansão de Testes Unitários (Session)** — ✅ Concluído
- **Task 2.1:** Implementar mocks para Firebase Auth em testes unitários de sessão. — ✅
- **Task 2.2:** Testar fluxos de expiração e revogação de tokens. — ✅
- **Task 2.3:** Testar criação de cookies com flags de segurança (HttpOnly/Secure). — ✅
- **UAT:** Coverage de `models/session.py` > 90%. (Atingido: 100%)

### Fase 2.1: Refatoração de Domínio (Value Objects & DTOs) (INSERTED)
Resolver obsessão primitiva e estruturar modelos com DDD.
- **Task 2.1.1:** Criar Value Objects para inputs primitivos (Topic, Knowledge, etc.).
- **Task 2.1.2:** Refatorar `models/user.py` e `models/prompt.py` para usar novos Value Objects.
- **Task 2.1.3:** Refatorar `models/session.py` para substituir `dict` por uma Entidade/DTO de User.
- **Task 2.1.4:** Refatorar `models/guide.py` para consistência de dados estruturados.
- **UAT:** 100% de aprovação nos testes unitários com os novos objetos.

### Fase 3: Auditoria e Refatoração de Erros Globais
Unificar a resposta de erro do sistema.
- **Task 3.1:** Mapear todos os pontos de integração (Gemini, Firebase) sem `try/except`.
- **Task 3.2:** Implementar mapeamento de erros 429/503 do Gemini para `ServiceError`.
- **Task 3.3:** Refatorar error handlers em `main.py` para cobrir novos casos.
- **UAT:** Nenhum erro não tratado vazando para o cliente nos logs.

### Fase 4: Desacoplamento da Lógica de Prompt
Tornar a orquestração de IA mais modular.
- **Task 4.1:** Extrair lógica de construção de mensagens de `models/prompt.py` para um serviço dedicado ou classe de fábrica.
- **Task 4.2:** Implementar validação de schema para as respostas geradas pelo Gemini antes de converter em DTO.
- **UAT:** Possibilidade de trocar o template do prompt sem alterar a lógica de processamento do modelo.

### Fase 5: Revisão de Estabilidade Final
- **Task 5.1:** Executar auditoria completa de coverage (meta global 90%).
- **Task 5.2:** Otimizar tempo de execução da suíte de testes (meta < 20s com VCR).
- **Task 5.3:** Documentar padrões de refatoração aplicados para futuras manutenções.
- **UAT:** Todos os 78+ testes passando de forma determinística e rápida.

---

## Próximos Passos
Após concluir o Milestone 1, o projeto estará pronto para novas funcionalidades de produto com uma base sólida.
