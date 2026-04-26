---
created: 2026-04-26T11:41:50Z
title: Project file audit and cleanup
area: tooling
files:
  - CLAUDE.md
  - .planning/
  - .agent/
---

## Problem

O repositório contém arquivos que podem ser desnecessários ou que precisam de uma política clara de versionamento. Especificamente:
- `CLAUDE.md` parece estar sem uso e "jogado" no projeto.
- Há dúvidas sobre se os arquivos do framework GSD (`.planning` e `.agent`) devem ser versionados no GitHub ou se deveriam ser locais/ignorados.
- É necessário um estudo sobre a "higiene" do repositório para evitar o acúmulo de arquivos "lixo".

## Solution

Realizar uma auditoria completa dos arquivos na raiz e nos diretórios ocultos do projeto:
1. Avaliar a utilidade do `CLAUDE.md` e outros arquivos similares.
2. Definir o que é essencial para o versionamento do estado do projeto (GSD) e o que pode ser gerado/local.
3. Executar a limpeza removendo arquivos obsoletos e atualizando o `.gitignore` se necessário.
