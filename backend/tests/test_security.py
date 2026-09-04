from fastapi.testclient import TestClient


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

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

    assert response.status_code == 200

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

    assert response.status_code == 201

    return response.json()["id"]


# ---------------------------------------------------------
# PROJECT AUTHORIZATION
# ---------------------------------------------------------

def test_user_cannot_access_another_users_project(client):
    user1 = register_and_login(
        client,
        "projectuser1",
        "project1@example.com",
    )

    user2 = register_and_login(
        client,
        "projectuser2",
        "project2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Project",
        "PRIVATE",
    )

    response = client.get(
        f"/api/projects/{project_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_project(client):
    user1 = register_and_login(
        client,
        "updateproject1",
        "updateproject1@example.com",
    )

    user2 = register_and_login(
        client,
        "updateproject2",
        "updateproject2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Project",
        "PRIVATE",
    )

    response = client.put(
        f"/api/projects/{project_id}",
        json={
            "name": "Hacked Project",
        },
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_project(client):
    user1 = register_and_login(
        client,
        "deleteproject1",
        "deleteproject1@example.com",
    )

    user2 = register_and_login(
        client,
        "deleteproject2",
        "deleteproject2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Project",
        "PRIVATE",
    )

    response = client.delete(
        f"/api/projects/{project_id}",
        headers=user2,
    )

    assert response.status_code == 404


# ---------------------------------------------------------
# BOOKMARK AUTHORIZATION
# ---------------------------------------------------------

def test_user_cannot_access_another_users_bookmark(client):
    user1 = register_and_login(
        client,
        "bookmarkuser1",
        "bookmark1@example.com",
    )

    user2 = register_and_login(
        client,
        "bookmarkuser2",
        "bookmark2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Bookmark Project",
        "BOOK",
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

    assert bookmark.status_code == 201

    bookmark_id = bookmark.json()["id"]

    response = client.get(
        f"/api/bookmarks/{bookmark_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_bookmark(client):
    user1 = register_and_login(
        client,
        "updatebookmark1",
        "updatebookmark1@example.com",
    )

    user2 = register_and_login(
        client,
        "updatebookmark2",
        "updatebookmark2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Bookmark Project",
        "BOOK",
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

    response = client.put(
        f"/api/bookmarks/{bookmark_id}",
        json={
            "title": "Hacked Bookmark",
        },
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_bookmark(client):
    user1 = register_and_login(
        client,
        "deletebookmark1",
        "deletebookmark1@example.com",
    )

    user2 = register_and_login(
        client,
        "deletebookmark2",
        "deletebookmark2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Bookmark Project",
        "BOOK",
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

    response = client.delete(
        f"/api/bookmarks/{bookmark_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_cannot_create_bookmark_in_another_users_project(client):
    user1 = register_and_login(
        client,
        "bookmarkproject1",
        "bookmarkproject1@example.com",
    )

    user2 = register_and_login(
        client,
        "bookmarkproject2",
        "bookmarkproject2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Project",
        "BOOK2",
    )

    response = client.post(
        "/api/bookmarks/",
        json={
            "project_id": project_id,
            "title": "Unauthorized Bookmark",
            "url": "https://example.com",
            "description": "Should fail",
        },
        headers=user2,
    )

    assert response.status_code == 404


# ---------------------------------------------------------
# NOTE AUTHORIZATION
# ---------------------------------------------------------

def test_user_cannot_access_another_users_note(client):
    user1 = register_and_login(
        client,
        "noteuser1",
        "note1@example.com",
    )

    user2 = register_and_login(
        client,
        "noteuser2",
        "note2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Notes",
        "NOTE",
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

    assert note.status_code == 201

    note_id = note.json()["id"]

    response = client.get(
        f"/api/notes/{note_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_note(client):
    user1 = register_and_login(
        client,
        "updatenote1",
        "updatenote1@example.com",
    )

    user2 = register_and_login(
        client,
        "updatenote2",
        "updatenote2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Notes",
        "NOTE2",
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

    response = client.put(
        f"/api/notes/{note_id}",
        json={
            "title": "Hacked Note",
        },
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_note(client):
    user1 = register_and_login(
        client,
        "deletenote1",
        "deletenote1@example.com",
    )

    user2 = register_and_login(
        client,
        "deletenote2",
        "deletenote2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Notes",
        "NOTE3",
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

    response = client.delete(
        f"/api/notes/{note_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_cannot_create_note_in_another_users_project(client):
    user1 = register_and_login(
        client,
        "noteproject1",
        "noteproject1@example.com",
    )

    user2 = register_and_login(
        client,
        "noteproject2",
        "noteproject2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Project",
        "NOTE4",
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


# ---------------------------------------------------------
# RESOURCE AUTHORIZATION
# ---------------------------------------------------------

def test_user_cannot_access_another_users_resource(client):
    user1 = register_and_login(
        client,
        "resourceuser1",
        "resource1@example.com",
    )

    user2 = register_and_login(
        client,
        "resourceuser2",
        "resource2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Resources",
        "RES",
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

    assert resource.status_code == 201

    resource_id = resource.json()["id"]

    response = client.get(
        f"/api/resources/{resource_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_resource(client):
    user1 = register_and_login(
        client,
        "updateresource1",
        "updateresource1@example.com",
    )

    user2 = register_and_login(
        client,
        "updateresource2",
        "updateresource2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Resources",
        "RES2",
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

    response = client.put(
        f"/api/resources/{resource_id}",
        json={
            "title": "Hacked Resource",
        },
        headers=user2,
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_resource(client):
    user1 = register_and_login(
        client,
        "deleteresource1",
        "deleteresource1@example.com",
    )

    user2 = register_and_login(
        client,
        "deleteresource2",
        "deleteresource2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Resources",
        "RES3",
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

    response = client.delete(
        f"/api/resources/{resource_id}",
        headers=user2,
    )

    assert response.status_code == 404


def test_cannot_create_resource_in_another_users_project(client):
    user1 = register_and_login(
        client,
        "resourceproject1",
        "resourceproject1@example.com",
    )

    user2 = register_and_login(
        client,
        "resourceproject2",
        "resourceproject2@example.com",
    )

    project_id = create_project(
        client,
        user1,
        "Private Project",
        "RES4",
    )

    response = client.post(
        "/api/resources/",
        json={
            "project_id": project_id,
            "title": "Unauthorized Resource",
            "description": "Should fail",
            "url": "https://example.com",
            "resource_type": "article",
        },
        headers=user2,
    )

    assert response.status_code == 404


# ---------------------------------------------------------
# AUTHENTICATION SECURITY
# ---------------------------------------------------------

def test_invalid_token_is_rejected(client):
    response = client.get(
        "/api/projects/",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_missing_token_is_rejected(client):
    response = client.get(
        "/api/projects/",
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