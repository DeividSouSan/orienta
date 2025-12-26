# Orienta — README Técnico

Orienta é uma aplicação full-stack para geração e gerenciamento de guias de estudo. O backend expõe uma API REST versionada e integra autenticação via Firebase, persistência via Firestore e geração/validação de conteúdo via Google GenAI (Gemini). O frontend é um Next.js exportado como site estático e servido pelo próprio backend.

## Visão de arquitetura

Este repositório segue um formato “mono” (monorepo) com dois blocos principais:

- **API** (Flask): responsável por autenticação, validações, geração de guias e acesso ao Firestore.
- **Web** (Next.js export): responsável pela UI e consumo da API via endpoint `/api/v1/*`.

O backend também atua como servidor de arquivos estáticos do build/export do Next (pasta `client/out`).

## Stack e tecnologias

### Backend

- Flask 3 (API REST)
- Firebase Admin SDK (criação/verificação de cookies de sessão e acesso ao Firestore)
- Google Cloud Firestore (persistência)
- Google GenAI (Gemini) para:
	- geração do guia em JSON com schema
	- validação semântica do tópico
- Pydantic v2 (`TypeAdapter`) para validar payloads (ex.: lista de estudos diários)
- Pytest (testes de integração via HTTP)

### Frontend

- Next.js (App Router) com `output: "export"` (build estático)
- React 19
- Tailwind CSS 4
- Radix UI primitives + `class-variance-authority` (componentização + variantes)
- Zod (validação no client)

### Ferramentas e qualidade

- `ruff` (lint/format no Python)
- `pre-commit` (ganchos locais)
- `commitizen` + Conventional Commits (higiene de histórico)
- ESLint + Prettier (front)

## Organização do código

- `main.py`: criação do app Flask, registro de blueprints e handlers de erro; também serve o build do frontend.
- `api/v1/*`: rotas versionadas (blueprints) por domínio.
- `models/*`: regras de negócio e integrações externas (Firestore, Firebase Auth, GenAI).
- `prompts/*`: prompts “source of truth” para geração/validação.
- `tests/integration/*`: testes de integração HTTP (black-box).

## Contratos HTTP (visão geral)

Os endpoints REST vivem sob o prefixo `/api/v1`.

- `GET /api/v1/status`: health check baseado em Firestore.
- `POST /api/v1/users`: cria usuário (Firebase Auth + registro no Firestore).
- `POST /api/v1/sessions`: login (Firebase REST) + criação de cookie de sessão.
- `DELETE /api/v1/sessions`: logout (remove cookie).
- `GET /api/v1/user`: retorna o usuário atual (requer cookie válido).
- `POST /api/v1/validate/topic`: valida topic (sintaxe + relevância via Gemini).
- `POST /api/v1/guides`: gera guia e persiste no Firestore.
- `GET /api/v1/guides`: lista guias do usuário.
- `GET /api/v1/guides/<id>`: recupera guia por id.
- `PATCH /api/v1/guides/<id>`: atualiza a lista de estudos (e status).
- `DELETE /api/v1/guides/<id>`: remove guia.

## Autenticação e sessão

Decisão: autenticação via **Firebase Auth** com sessão baseada em **cookie HTTP-only**.

- Login (`POST /sessions`) autentica via **Firebase Identity Toolkit REST** e recebe um `idToken`.
- O backend converte o `idToken` em um **session cookie** (`auth.create_session_cookie`).
- O cookie é gravado como `session_id` com:
	- `HttpOnly` (mitiga XSS lendo token)
	- `Secure` apenas em produção (`ENVIRONMENT == "production"`)
	- `Path=/` e TTL de 14 dias (`DURATION_IN_SECONDS`)

O client não gerencia tokens diretamente; a sessão é transparente via cookie (boa ergonomia e melhor postura de segurança). Em compensação, CORS/CSRF exigem atenção em deploy real (ver seção “Segurança”).

## Persistência e modelagem (Firestore)

Decisão: usar Firestore como banco “document-oriented” para reduzir fricção operacional (busca-se substituir por um banco SQL em breve).

Coleções:

- `users`: cadastro de usuários com `username/email/uid/created_at`.
- `users_guides`: guias gerados por usuário; contém metadados (modelo, tempo, inputs), conteúdo (`daily_study`) e status.
- `_internal_status`: usado no bootstrap como health check.

Observação: o backend aplica autorização no nível de documento (ex.: ao excluir estudos, valida se `owner == username`).

## Geração e validação via IA (Gemini)

### Geração do guia

Decisão: produzir saída do modelo como JSON validável.

- O system prompt é carregado de `prompts/generate_guide.md`.
- A chamada ao Gemini define `response_mime_type: application/json` e `response_schema` (lista de `DailyStudySchema`).
- Há fallback de modelos (ex.: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.0-flash`) com retry em 503/429.

Isso minimiza pós-processamento textual e reduz risco de “resposta não parseável” (quando o modelo alucina).

### Validação do tópico

Decisão: validação em duas etapas:

1) **Sintática**: tamanho/estrutura e campos (ex.: topic entre 10 e 150 chars).
2) **Semântica**: chamada ao Gemini com schema `ValidationResult` (relevância, linguagem inadequada, gibberish) usando `temperature: 0`.

## Servindo o frontend (Next export) pelo Flask

O frontend é exportado (`output: "export"`) e servido de `client/out` pelo Flask (`static_folder="client/out"`). O handler de rota “catch-all” tenta:

1) servir o arquivo exato (`/path`)
2) servir `/path.html`
3) fallback para `index.html`

Há também a decisão de separar o tratamento de 404:

- Para rotas `/api/*`, retorna JSON estruturado `NotFoundError`.
- Para demais rotas, redireciona para `/` (comportamento de SPA estática; o router do Next lida com a renderização).

### Trailing slash

O Next está configurado com `trailingSlash: true`. Isso influencia:

- URLs do frontend tendem a ser do formato `/rota/`.
- Componentes do client devem normalizar pathname para detectar rota ativa (ex.: remover apenas a `/` final para comparação).

## Erros e observabilidade

O backend usa uma camada de exceções de domínio em `errors.py`:

- `ValidationError` (400)
- `UnauthorizedError` (401)
- `NotFoundError` (404)
- `ConflictError` (409)
- `MethodNotAllowed` (405)
- `ServiceError` (503)
- `InternalServerError` (500)

Em `main.py`, o handler global:

- converte exceções “conhecidas” para JSON (`toDict()`)
- transforma qualquer exceção não mapeada em `InternalServerError`

Trade-off: é uma estratégia simples e consistente de contrato de erro (boa DX no client).

## Segurança (postura e decisões)

- Cookie de sessão `HttpOnly` reduz exposição do token a XSS.
- Verificação `check_revoked=True` dá suporte a invalidação de sessão.
- Autorização no backend valida ownership para operações críticas (ex.: update/delete de guias).

## Testes

Os testes são de **integração HTTP** (pasta `tests/integration`), consumindo a API via `requests` e uma variável `API_URL`.

- Cobrem status, usuários, sessão, validate topic e CRUD de guides.
- A abordagem black-box valida contratos (status code + shape do JSON), ideal para evitar testes acoplados ao framework.

## Decisões e trade-offs principais

- **Next export + Flask servindo estático**: simplifica deploy e manutenção do projeto (um repositório, um serviço), mas dificulta a implementação de rotas dinâmicas e features que dependem de server-side do Next.
- **Firestore**: reduz overhead operacional e integra bem com Firebase, mas exige atenção a consistência/consultas e índices (será substituido por tabelas futuramente).
- **IA com schema**: melhora robustez do parse e validação; ainda exige fallback e tratamento de quotas/429.
- **Sessão via cookie**: melhora UX e segurança;

