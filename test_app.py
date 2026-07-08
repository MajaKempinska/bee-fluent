import pytest
from app import app, normalize


@pytest.fixture
def client():
    """Tworzy testowego klienta Flaska, przez którego odpytujemy endpointy."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- Testy funkcji normalize ---

def test_normalize_lowercase():
    assert normalize("HELLO World") == "hello world"

def test_normalize_removes_punctuation():
    assert normalize("does she drink coffee?") == "does she drink coffee"
    assert normalize("she is late.") == "she is late"

def test_normalize_collapses_spaces():
    assert normalize("he   plays    football") == "he plays football"


# --- Testy endpointu /health ---

def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


# --- Testy endpointu /questions ---

def test_questions_returns_list(client):
    response = client.get("/questions")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_questions_hide_answers(client):
    response = client.get("/questions")
    data = response.get_json()
    for question in data:
        assert "answer" not in question


# --- Testy endpointu /check ---

def test_check_correct_answer(client):
    response = client.post("/check", json={"id": 3, "answer": "like"})
    assert response.status_code == 200
    assert response.get_json()["correct"] is True

def test_check_wrong_answer(client):
    response = client.post("/check", json={"id": 3, "answer": "likes"})
    assert response.get_json()["correct"] is False

def test_check_apostrophe_answer(client):
    response = client.post("/check", json={"id": 10, "answer": "he doesn't play football"})
    assert response.get_json()["correct"] is True

def test_check_full_form_accepted(client):
    response = client.post("/check", json={"id": 10, "answer": "he does not play football"})
    assert response.get_json()["correct"] is True

def test_check_missing_fields(client):
    response = client.post("/check", json={})
    assert response.status_code == 400