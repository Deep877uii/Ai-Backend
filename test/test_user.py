from .database import client


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome Deepu"}

def test_create_user(client):
    response = client.post("/users/", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"email": "test@example.com"}
