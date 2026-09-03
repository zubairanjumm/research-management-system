from fastapi.testclient import TestClient


def register_and_login(client, username, email):
    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "password123",
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_project(client, headers, name="Test Project", symbol="TEST"):
    response = client.post(
        "/api/projects/",
        json={
            "name": name,
            "symbol": symbol,
            "description": "Test project",
        },
        headers=headers,
    )

    return response.json()["id"]


def test_user_cannot_access_another_users_bookmark(client):
    user1 = register_and_login(
        client, "securityuser1", "security1@example.com"
    )
    user2 = register_and_login(
        client, "securityuser2", "security2@example.com"
    )

    project_id = create_project(
        client, user1, "User 1 Project", "USER1"
    )

    bookmark = client.post(
        "/api/bookmarks/",
        json={
            "project_id": project_id,
            "title": "Private Bookmark",
            "url": "https://example.com",
            "description": "Private",
        },
        headers=user1,
    )

    bookmark_id = bookmark.json()["id"]

    response = client.get(
        f"/api/bookmarks/{bookmark_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_access_another_users_note(client):
    user1 = register_and_login(
        client, "securitynote1", "securitynote1@example.com"
    )
    user2 = register_and_login(
        client, "securitynote2", "securitynote2@example.com"
    )

    project_id = create_project(
        client, user1, "Private Notes", "NOTE1"
    )

    note = client.post(
        "/api/notes/",
        json={
            "project_id": project_id,
            "title": "Private Note",
            "content": "Private content",
        },
        headers=user1,
    )

    note_id = note.json()["id"]

    response = client.get(
        f"/api/notes/{note_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_access_another_users_resource(client):
    user1 = register_and_login(
        client, "securityresource1", "securityresource1@example.com"
    )
    user2 = register_and_login(
        client, "securityresource2", "securityresource2@example.com"
    )

    project_id = create_project(
        client, user1, "Private Resources", "RES1"
    )

    resource = client.post(
        "/api/resources/",
        json={
            "project_id": project_id,
            "title": "Private Resource",
            "description": "Private resource",
            "url": "https://example.com",
            "resource_type": "article",
        },
        headers=user1,
    )

    resource_id = resource.json()["id"]

    response = client.get(
        f"/api/resources/{resource_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_cannot_create_note_in_another_users_project(client):
    user1 = register_and_login(
        client, "securityproject1", "securityproject1@example.com"
    )
    user2 = register_and_login(
        client, "securityproject2", "securityproject2@example.com"
    )

    project_id = create_project(
        client, user1, "User 1 Project", "PROJ1"
    )

    response = client.post(
        "/api/notes/",
        json={
            "project_id": project_id,
            "title": "Unauthorized Note",
            "content": "Should fail",
        },
        headers=user2,
    )

    assert response.status_code == 404


def test_invalid_token_is_rejected(client):
    response = client.get(
        "/api/projects/",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_duplicate_username_is_rejected(client):
    client.post(
        "/auth/register",
        json={
            "username": "duplicateuser",
            "email": "first@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "duplicateuser",
            "email": "second@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409


def test_duplicate_email_is_rejected(client):
    client.post(
        "/auth/register",
        json={
            "username": "firstuser",
            "email": "duplicate@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "seconduser",
            "email": "duplicate@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409