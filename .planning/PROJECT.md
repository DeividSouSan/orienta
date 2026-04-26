# Project: Orienta

## What This Is
Orienta é uma plataforma que utiliza Inteligência Artificial (Google Gemini) para criar planos de estudo personalizados. O sistema permite que usuários definam tópicos, nível de conhecimento e tempo disponível para receber um cronograma estruturado de aprendizado.

## Mission
Transformar a maneira como as pessoas aprendem qualquer tópico, fornecendo roteiros estruturados e personalizados, mantendo uma base de código de alta qualidade, estável e fácil de manter.

## Core Values
- **Estabilidade:** Garantir que o sistema seja confiável e resiliente a falhas de APIs externas.
- **Manutenibilidade:** Código limpo, arquitetura desacoplada e documentação viva.
- **Qualidade Técnica:** Alta cobertura de testes e validações rigorosas.

## Context
O projeto está em fase de **manutenção e refatoração**. As funcionalidades principais já estão implementadas, e o foco agora é a melhoria contínua da arquitetura e a garantia de estabilidade através de testes e auditorias.

## Requirements

### Validated
- ✓ **Geração de Guias:** Criação de roteiros de estudo com metadados via Gemini API.
- ✓ **Autenticação:** Sistema de login, registro e persistência de sessão via Firebase Auth.
- ✓ **Persistência:** Armazenamento e recuperação de guias no Google Firestore.
- ✓ **Validação de Entrada:** Validação de tópicos e viabilidade de estudo via IA.
- ✓ **Infraestrutura de Testes:** Integração com VCR para gravação de chamadas de API e Pytest para execução.
- ✓ **DTOs & Value Objects:** Camada de transporte e domínio isolada para validação de dados.

### Active
- [ ] **Cobertura de Testes:** Alcançar >90% de cobertura, focando em `models/prompt.py` e `models/session.py`.
- [ ] **Tratamento de Erros:** Unificar e expandir os error handlers globais para cobrir casos de borda do Gemini/Firestore.
- [ ] **Refatoração de IA:** Isolar ainda mais a lógica de prompts e modelos para facilitar a troca/atualização de LLMs.

### Out of Scope
- Novas funcionalidades de produto (social, gamificação, exportação) neste ciclo de manutenção.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| **VCR para Testes** | Evitar custos de API e instabilidade de rede nos testes de integração. | Implementado |
| **Model Cycling** | Alternar entre modelos Gemini (Flash, Flash-Lite) para contornar rate limits do free-tier. | Implementado |
| **Arquitetura em Camadas** | Facilitar a manutenção e testes unitários através do desacoplamento (API/DTO/Model/Object). | Em evolução |

## Evolution
Este documento evolui conforme novas refatorações são concluídas e a estabilidade do sistema aumenta.

---
*Last updated: 2026-04-26 after initialization*
