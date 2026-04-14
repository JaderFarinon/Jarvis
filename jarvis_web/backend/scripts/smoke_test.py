"""Smoke tests para validar integração local do Jarvis Web backend."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.services import assistant_service


def _assert_status(response, status: int, label: str) -> None:
    assert response.status_code == status, f"{label} falhou: {response.status_code} -> {response.text}"


def run() -> None:
    observed = {}

    def fake_chat_completion(**kwargs):
        observed["api_key"] = kwargs["api_key"]
        observed["model"] = kwargs["model"]
        observed["context"] = kwargs["context"]
        return {
            "resposta_texto": "Resposta mockada com contexto do banco.",
            "acao_detectada": "general_question",
            "entidade": None,
            "dados_extraidos": {},
            "precisa_confirmacao": False,
        }

    assistant_service.build_chat_completion = fake_chat_completion

    with TestClient(app) as client:
        _assert_status(client.get("/api/health"), 200, "health")

        settings_payload = {"openai_api_key": "sk-local-test", "openai_model": "gpt-4.1-mini"}
        settings_response = client.put("/api/settings/openai", json=settings_payload)
        _assert_status(settings_response, 200, "settings upsert")
        assert settings_response.json()["openai_api_key"] == "sk-local-test"

        entities = [
            (
                "tasks",
                {
                    "title": "Task smoke",
                    "description": "Teste",
                    "priority": "medium",
                    "status": "pending",
                    "due_date": "2026-04-20",
                },
            ),
            (
                "appointments",
                {
                    "title": "Appointment smoke",
                    "description": "Teste",
                    "date": "2026-04-20",
                    "time": "10:00",
                    "location": "Online",
                    "status": "scheduled",
                },
            ),
            (
                "notes",
                {"title": "Note smoke", "content": "Conteúdo", "tag": "smoke"},
            ),
            (
                "expenses",
                {
                    "description": "Expense smoke",
                    "amount": 12.5,
                    "category": "tests",
                    "expense_date": "2026-04-20",
                    "payment_method": "pix",
                    "notes": "smoke",
                },
            ),
            (
                "reminders",
                {
                    "title": "Reminder smoke",
                    "description": "Teste",
                    "remind_at": "2026-04-20T10:00:00",
                    "status": "pending",
                },
            ),
        ]

        for module, payload in entities:
            created = client.post(f"/api/{module}", json=payload)
            _assert_status(created, 201, f"create {module}")
            entity_id = created.json()["id"]

            listed = client.get(f"/api/{module}")
            _assert_status(listed, 200, f"list {module}")
            assert any(item["id"] == entity_id for item in listed.json())

            updated = client.put(f"/api/{module}/{entity_id}", json=payload)
            _assert_status(updated, 200, f"update {module}")

            deleted = client.delete(f"/api/{module}/{entity_id}")
            _assert_status(deleted, 204, f"delete {module}")

        context_response = client.get("/api/assistant/context")
        _assert_status(context_response, 200, "assistant context")
        context_data = context_response.json()
        assert "tarefas_pendentes" in context_data
        assert "proximos_compromissos" in context_data

        chat_response = client.post("/api/assistant/chat", json={"message": "Resumo do meu dia"})
        _assert_status(chat_response, 200, "assistant chat")
        assert observed.get("api_key") == "sk-local-test"
        assert isinstance(observed.get("context"), dict)


if __name__ == "__main__":
    run()
    print("Smoke test finalizado com sucesso.")
