---
created: 2026-04-26T08:35:12Z
title: Fix typos in prompt model and tests
area: models
files:
  - models/prompt.py
  - tests/unit/models/test_prompt.py
---

## Problem

O usuário identificou erros de escrita (typos) tanto no arquivo de modelo `models/prompt.py` quanto nos testes unitários recém-criados em `tests/unit/models/test_prompt.py`. Esses erros afetam a qualidade do código e da documentação interna.

## Solution

Revisar ambos os arquivos em busca de erros ortográficos em português e inglês (mensagens de erro, asserts e comentários) e corrigi-los.
- Exemplo notado: `consegiu` em vez de `conseguiu` em `prompt.py`.
- Exemplo notado: `Arendizado` em vez de `Aprendizado` em `test_prompt.py`.
