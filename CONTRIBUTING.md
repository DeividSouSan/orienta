# Sobre Contribuições

O **Orienta** é um projeto pessoal e de código aberto. Embora o código esteja disponível publicamente, **este repositório não aceita contribuições externas** (Pull Requests não serão aceitos).

## 🆓 O que você pode fazer

Você tem total liberdade para:

- ✅ **Forkar** o repositório
- ✅ **Clonar** o projeto
- ✅ **Modificar** o código como quiser
- ✅ **Usar** como base para seus próprios projetos
- ✅ **Aprender** com a implementação

## 🍴 Fork e Clone

### 1. Faça o fork do repositório

Clique no botão **Fork** no canto superior direito da página do repositório no GitHub.

### 2. Clone o seu fork

```bash
git clone https://github.com/SEU_USUARIO/orienta-api.git
cd orienta-api
```

A partir daqui, o projeto é seu! Faça as alterações que desejar.

---

## 🚀 Como Rodar o Projeto

### 📋 Pré-requisitos

- **Python 3.11+**
- **Node.js 20+** e **npm**
- **Git**
- Conta no **Firebase** (para obter as credenciais)
- Chave de API do **Google GenAI (Gemini)**

---

## ⚙️ Backend (Python/Flask)

### 1. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
ENVIRONMENT=development
FIREBASE_API_KEY=sua_chave_api_firebase
GOOGLE_GENAI_API_KEY=sua_chave_api_gemini
GENERATION_MODEL=gemini-2.5-flash|gemini-2.5-flash-lite
VALIDATION_MODEL=gemini-2.5-flash-lite|gemini-2.5-flash
```

> ⚠️ **Importante:** Os modelos `GENERATION_MODEL` e `VALIDATION_MODEL` devem ser especificados manualmente, separando-os por meio do caractere Pipe (|). O Google frequentemente altera quais modelos estão disponíveis no Free Tier, então consulte a [documentação oficial do Gemini](https://ai.google.dev/models) para verificar quais modelos estão disponíveis no momento.

### 4. Configure o Firebase

Coloque o arquivo `service-account.json` do Firebase na raiz do projeto. Você pode obtê-lo no console do Firebase:

1. Acesse o [Console do Firebase](https://console.firebase.google.com/)
2. Vá em **Configurações do projeto** > **Contas de serviço**
3. Clique em **Gerar nova chave privada**
4. Renomeie o arquivo baixado para `service-account.json`

### 5. Execute o servidor

```bash
flask --app main run --debug
```

O backend estará disponível em `http://localhost:5000`.

---

## 🎨 Frontend (Next.js)

### 1. Navegue até a pasta do cliente

```bash
cd client
```

### 2. Instale as dependências

```bash
npm install
```

### 3. Execute o servidor de desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`.

---

## 🧪 Executando os Testes

```bash
# Na raiz do projeto
pytest
```

---

## 📁 Estrutura do Projeto

```
orienta-api/
├── api/v1/           # Rotas da API (blueprints Flask)
├── models/           # Modelos e regras de negócio
├── prompts/          # Prompts para o Gemini
├── tests/            # Testes de integração
├── client/           # Frontend Next.js
│   ├── src/
│   │   ├── app/      # Páginas (App Router)
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── hooks/
│   │   └── services/
│   └── public/
├── main.py           # Entry point do Flask
├── requirements.txt  # Dependências Python
└── README.md
```

---

**Aproveite o projeto!** 🎉
