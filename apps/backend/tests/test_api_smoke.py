import os

os.environ["QUESTION_TOKEN_SECRET"] = "test-secret"
os.environ["SESSION_PERSISTENCE_ENABLED"] = "false"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_question_then_validate():
    question_response = client.get(
        "/api/v1/questions",
        params={"module": "integer-operations", "difficulty": "easy"},
    )
    assert question_response.status_code == 200
    question = question_response.json()

    from app.core.security import verify_question_payload

    payload = verify_question_payload(question["validation_token"])

    validate_response = client.post(
        "/api/v1/answers/validate",
        json={
            "session_id": "ephemeral-session",
            "module": question["module"],
            "difficulty": question["difficulty"],
            "question_id": question["question_id"],
            "validation_token": question["validation_token"],
            "user_answer": payload["expected_answer"],
        },
    )
    assert validate_response.status_code == 200
    assert validate_response.json()["is_correct"] is True
