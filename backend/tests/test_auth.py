from fastapi.testclient import TestClient

from app.main import app



def test_root(client):
    response = client.get("/")

    assert response.status_code == 200


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data

def test_login(client):
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "loginuser",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_me(client):
    client.post(
        "/auth/register",
        json={
            "username": "meuser",
            "email": "me@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "meuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "meuser"


def test_user_cannot_access_another_users_project(client):
    # User 1
    client.post(
        "/auth/register",
        json={
            "username": "userone",
            "email": "userone@example.com",
            "password": "password123",
        },
    )

    login1 = client.post(
        "/auth/login",
        data={"username": "userone", "password": "password123"},
    )
    token1 = login1.json()["access_token"]

    project = client.post(
        "/api/projects/",
        json={
            "name": "User One Project",
            "symbol": "USER1",
            "description": "Private project",
        },
        headers={"Authorization": f"Bearer {token1}"},
    )

    project_id = project.json()["id"]

    # User 2
    client.post(
        "/auth/register",
        json={
            "username": "usertwo",
            "email": "usertwo@example.com",
            "password": "password123",
        },
    )

    login2 = client.post(
        "/auth/login",
        data={"username": "usertwo", "password": "password123"},
    )
    token2 = login2.json()["access_token"]

    # User 2 tries to access User 1's project
    response = client.get(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert response.status_code == 404