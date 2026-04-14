# Jarvis Web Backend

Para instruções completas de execução de backend + frontend no Debian/Ubuntu, consulte:

- `../README.md`

## Execução rápida apenas do backend

```bash
cd jarvis_web/backend
python3 -m venv .venv
source .venv/bin/activate
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Smoke test local

```bash
cd jarvis_web/backend
PYTHONPATH=. python3 scripts/smoke_test.py
```
