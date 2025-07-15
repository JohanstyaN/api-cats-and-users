import pytest

def test_list_users_empty(client):
    r = client.get("/users")
    assert r.status_code == 200
    assert r.json() == []

def test_create_user_and_list(client):
    payload = {
        "name":      "Test",
        "last_name": "User",
        "password":  "secret123"
    }
    
    r = client.post("/users", json=payload)
    assert r.status_code == 201
    u = r.json()
    assert u["name"] == "Test"
    assert "username" in u and u["username"] == "test.user"
    assert "id" in u

    r2 = client.get("/users")
    assert r2.status_code == 200
    users = r2.json()
    assert len(users) == 1
    assert users[0]["username"] == "test.user"

def test_login_success(client):
    client.post("/users", json={"name":"A","last_name":"B","password":"pw"})
    r = client.get("/users/login?username=a.b&password=pw")
    assert r.status_code == 200
    assert r.json()["username"] == "a.b"

def test_login_fail(client):
    r = client.get("/users/login?username=foo&password=bar")
    assert r.status_code == 401
