# jarvis_web (FastAPI + Vue + SQLite)

Projeto full-stack do assistente Jarvis, pronto para execução local com backend FastAPI, frontend Vue/Vite e banco SQLite criado automaticamente.

## Stack

- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: Vue 3 + Vite + Tailwind
- IA: OpenAI API (chave persistida no SQLite)

---

## Execução local (Debian/Ubuntu)

### 1) Pré-requisitos do sistema

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm
```

### 2) Backend

```bash
cd jarvis_web/backend
python3 -m venv .venv
source .venv/bin/activate
cp .env.example .env
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend disponível em:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

### 3) Frontend (em outro terminal)

```bash
cd jarvis_web/frontend
cp .env.example .env
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Frontend disponível em:

- `http://localhost:5173`

---

## Banco SQLite automático

- O backend usa `DATABASE_URL=sqlite:///./jarvis_web.db` por padrão.
- Ao iniciar o FastAPI, ele:
  1. cria a pasta do arquivo (se necessário),
  2. cria o arquivo SQLite (se não existir),
  3. cria as tabelas automaticamente,
  4. aplica seed inicial opcional (`DATABASE_SEED_ENABLED=true`) quando banco está vazio.

---

## Fluxo de configuração da OpenAI

1. Abra o frontend em `/configuracoes`.
2. Salve `openai_api_key` e `openai_model`.
3. O backend persiste no SQLite (`settings`) e usa essa chave nas chamadas do chat (`/api/assistant/chat`).

---

## Rotas principais

- Saúde: `GET /api/health`
- OpenAI settings: `GET|PUT /api/settings/openai`
- Assistente:
  - `GET /api/assistant/context`
  - `POST /api/assistant/chat`
- CRUD:
  - `tasks`: `GET|POST /api/tasks`, `PUT|DELETE /api/tasks/{id}`
  - `appointments`: `GET|POST /api/appointments`, `PUT|DELETE /api/appointments/{id}`
  - `notes`: `GET|POST /api/notes`, `PUT|DELETE /api/notes/{id}`
  - `expenses`: `GET|POST /api/expenses`, `PUT|DELETE /api/expenses/{id}`
  - `reminders`: `GET|POST /api/reminders`, `PUT|DELETE /api/reminders/{id}`

---

## Verificação rápida (smoke test)

Com backend dependencies instaladas:

```bash
cd jarvis_web/backend
PYTHONPATH=. python3 scripts/smoke_test.py
```

Esse script valida:

- healthcheck,
- gravação/leitura de configurações OpenAI,
- CRUD de tarefas/compromissos/notas/gastos/lembretes,
- contexto do assistente,
- chat chamando backend e usando chave salva no banco.

