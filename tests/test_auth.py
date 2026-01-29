from app.schemas.user import UserCreate


def test_register_and_login(client):
    response = client.post("/api/auth/register", json=UserCreate(username="alice", password="secret123").model_dump())
    assert response.status_code == 200
    login = client.post("/api/auth/login", json=UserCreate(username="alice", password="secret123").model_dump())
    assert login.status_code == 200
    assert "access_token" in login.json()
