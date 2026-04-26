---
created: 2026-04-26T11:38:15Z
title: Study refactoring models into Value Objects
area: architecture
files:
  - models/prompt.py
  - models/session.py
  - models/user.py
  - models/guide.py
---

## Problem

A estrutura atual dos models pode ser aprimorada seguindo padrões de Domain-Driven Design (DDD). Atualmente, `prompt.py` e os inputs do usuário ('topic', 'knowledge', etc.) são tratados de forma procedimental ou como dicionários simples, o que dificulta a manutenção e a validação consistente em larga escala.

## Solution

Estudar e planejar uma refatoração profunda para transformar os models em Value Objects:
- `Prompt` como um Value Object que compõe um `Guide`.
- Campos de User Input (Topic, Knowledge, FocusTime, Days) como Value Objects individuais com suas próprias regras de validação encapsuladas.
- `User` em `models/session.py`: substituir `dict` por uma Entidade ou DTO estruturado para evitar ambiguidades.
- `models/user.py`: resolver "obsessão primitiva" transformando `username`, `email` e `password` em Value Objects dedicados.
- `models/guide.py`: aplicar Value Objects e DTOs para estruturar os dados do guia e seus subcomponentes, eliminando a obsessão primitiva.
- Isso permitiria remover as funções de validação avulsas em favor de objetos que garantem sua própria validade na criação.
