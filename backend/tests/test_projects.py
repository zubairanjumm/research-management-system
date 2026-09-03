def test_create_project(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "username": "projectuser",
            "email": "project@example.com",
            "password": "password123",
        },
    )

    # Login
    login = client.post(
        "/auth/login",
        data={
            "username": "projectuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "name": "My Research Project",
            "symbol": "RESEARCH",
            "description": "Testing project creation",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Research Project"
    assert data["symbol"] == "RESEARCH"



def test_get_projects(client):
    client.post(
        "/auth/register",
        json={
            "username": "getuser",
            "email": "get@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "getuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    client.post(
        "/api/projects/",
        json={
            "name": "My Project",
            "symbol": "MYPROJ",
            "description": "Test project",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/api/projects/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "My Project"


def test_update_project(client):
    client.post(
        "/auth/register",
        json={
            "username": "updateuser",
            "email": "update@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "updateuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Old Name",
            "symbol": "OLD",
            "description": "Old description",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    response = client.put(
        f"/api/projects/{project_id}",
        json={
            "name": "New Name",
            "symbol": "NEW",
            "description": "New description",
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["symbol"] == "NEW"



def test_delete_project(client):
    client.post(
        "/auth/register",
        json={
            "username": "deleteuser",
            "email": "delete@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "deleteuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Project To Delete",
            "symbol": "DELETE",
            "description": "Temporary project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    response = client.delete(
        f"/api/projects/{project_id}",
        headers=headers,
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/projects/{project_id}",
        headers=headers,
    )

    assert response.status_code == 404

def test_projects_require_authentication(client):
    response = client.get("/api/projects/")

    assert response.status_code == 401

def test_project_update_requires_authentication(client):
    response = client.put(
        "/api/projects/1",
        json={
            "name": "Updated",
            "symbol": "UPD",
            "description": "Updated project",
        },
    )

    assert response.status_code == 401


def test_user_cannot_update_another_users_project(client):
    # User 1
    client.post(
        "/auth/register",
        json={
            "username": "owner",
            "email": "owner@example.com",
            "password": "password123",
        },
    )

    login1 = client.post(
        "/auth/login",
        data={"username": "owner", "password": "password123"},
    )
    token1 = login1.json()["access_token"]

    project = client.post(
        "/api/projects/",
        json={
            "name": "Private Project",
            "symbol": "PRIV",
            "description": "Owner project",
        },
        headers={"Authorization": f"Bearer {token1}"},
    )

    project_id = project.json()["id"]

    # User 2
    client.post(
        "/auth/register",
        json={
            "username": "attacker",
            "email": "attacker@example.com",
            "password": "password123",
        },
    )

    login2 = client.post(
        "/auth/login",
        data={"username": "attacker", "password": "password123"},
    )
    token2 = login2.json()["access_token"]

    response = client.put(
        f"/api/projects/{project_id}",
        json={
            "name": "Hacked Project",
            "symbol": "HACK",
            "description": "Unauthorized update",
        },
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert response.status_code == 404



def test_user_cannot_delete_another_users_project(client):
    # User 1
    client.post(
        "/auth/register",
        json={
            "username": "deleteowner",
            "email": "deleteowner@example.com",
            "password": "password123",
        },
    )

    login1 = client.post(
        "/auth/login",
        data={
            "username": "deleteowner",
            "password": "password123",
        },
    )
    token1 = login1.json()["access_token"]

    project = client.post(
        "/api/projects/",
        json={
            "name": "Protected Project",
            "symbol": "PROT",
            "description": "Should not be deleted",
        },
        headers={"Authorization": f"Bearer {token1}"},
    )

    project_id = project.json()["id"]

    # User 2
    client.post(
        "/auth/register",
        json={
            "username": "deleteattacker",
            "email": "deleteattacker@example.com",
            "password": "password123",
        },
    )

    login2 = client.post(
        "/auth/login",
        data={
            "username": "deleteattacker",
            "password": "password123",
        },
    )
    token2 = login2.json()["access_token"]

    response = client.delete(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert response.status_code == 404

def test_create_bookmark(client):
    client.post(
        "/auth/register",
        json={
            "username": "bookmarkuser",
            "email": "bookmark@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "bookmarkuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Bookmark Project",
            "symbol": "BOOK",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    response = client.post(
        "/api/bookmarks/",
        json={
            "title": "FastAPI Docs",
            "url": "https://fastapi.tiangolo.com/",
            "description": "FastAPI documentation",
            "project_id": project_id,
        },
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["title"] == "FastAPI Docs"


def test_get_bookmarks(client):
    client.post(
        "/auth/register",
        json={
            "username": "getbookmark",
            "email": "getbookmark@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "getbookmark",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Bookmark Project",
            "symbol": "GETBOOK",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    client.post(
        "/api/bookmarks/",
        json={
            "title": "Python",
            "url": "https://python.org/",
            "description": "Python website",
            "project_id": project_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/bookmarks/",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python"


def test_update_bookmark(client):
    client.post(
        "/auth/register",
        json={
            "username": "updatebookmark",
            "email": "updatebookmark@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "updatebookmark",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Update Project",
            "symbol": "UPDATE",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    bookmark = client.post(
        "/api/bookmarks/",
        json={
            "title": "Old Title",
            "url": "https://example.com/",
            "description": "Old description",
            "project_id": project_id,
        },
        headers=headers,
    )

    bookmark_id = bookmark.json()["id"]

    response = client.put(
        f"/api/bookmarks/{bookmark_id}",
        json={
            "title": "New Title",
            "url": "https://example.org/",
            "description": "New description",
            "project_id": project_id,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_delete_bookmark(client):
    client.post(
        "/auth/register",
        json={
            "username": "deletebookmark",
            "email": "deletebookmark@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "deletebookmark",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Delete Project",
            "symbol": "DELETE",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    bookmark = client.post(
        "/api/bookmarks/",
        json={
            "title": "Delete Me",
            "url": "https://example.com/",
            "description": "Temporary bookmark",
            "project_id": project_id,
        },
        headers=headers,
    )

    bookmark_id = bookmark.json()["id"]

    response = client.delete(
        f"/api/bookmarks/{bookmark_id}",
        headers=headers,
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/bookmarks/{bookmark_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_bookmarks_require_authentication(client):
    response = client.get("/api/bookmarks/")

    assert response.status_code == 401



def test_create_note(client):
    client.post(
        "/auth/register",
        json={
            "username": "noteuser",
            "email": "note@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "noteuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Notes Project",
            "symbol": "NOTE",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    response = client.post(
        "/api/notes/",
        json={
            "title": "My First Note",
            "content": "This is a test note.",
            "project_id": project_id,
        },
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["title"] == "My First Note"
    assert response.json()["content"] == "This is a test note."


def test_get_notes(client):
    client.post(
        "/auth/register",
        json={
            "username": "getnote",
            "email": "getnote@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "getnote",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Get Notes Project",
            "symbol": "GETNOTE",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    client.post(
        "/api/notes/",
        json={
            "title": "Python Notes",
            "content": "Python content",
            "project_id": project_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/notes/",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python Notes"


def test_update_note(client):
    client.post(
        "/auth/register",
        json={
            "username": "updatenote",
            "email": "updatenote@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "updatenote",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Update Notes Project",
            "symbol": "UPNOTE",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    note = client.post(
        "/api/notes/",
        json={
            "title": "Old Title",
            "content": "Old content",
            "project_id": project_id,
        },
        headers=headers,
    )

    note_id = note.json()["id"]

    response = client.put(
        f"/api/notes/{note_id}",
        json={
            "title": "New Title",
            "content": "New content",
            "project_id": project_id,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["content"] == "New content"


def test_delete_note(client):
    client.post(
        "/auth/register",
        json={
            "username": "deletenote",
            "email": "deletenote@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "deletenote",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Delete Notes Project",
            "symbol": "DELNOTE",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    note = client.post(
        "/api/notes/",
        json={
            "title": "Delete Me",
            "content": "Temporary note",
            "project_id": project_id,
        },
        headers=headers,
    )

    note_id = note.json()["id"]

    response = client.delete(
        f"/api/notes/{note_id}",
        headers=headers,
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/notes/{note_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_notes_require_authentication(client):
    response = client.get("/api/notes/")

    assert response.status_code == 401


def test_create_resource(client):
    client.post(
        "/auth/register",
        json={
            "username": "resourceuser",
            "email": "resource@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "resourceuser",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Resource Project",
            "symbol": "RES",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    response = client.post(
        "/api/resources/",
        json={
            "title": "FastAPI Resource",
            "url": "https://fastapi.tiangolo.com/",
            "description": "FastAPI documentation",
            "resource_type": "documentation",
            "project_id": project_id,
        },
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["title"] == "FastAPI Resource"
    assert response.json()["resource_type"] == "documentation"


def test_get_resources(client):
    client.post(
        "/auth/register",
        json={
            "username": "getresource",
            "email": "getresource@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "getresource",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Get Resources Project",
            "symbol": "GETRES",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    client.post(
        "/api/resources/",
        json={
            "title": "Python Resource",
            "url": "https://python.org/",
            "description": "Python website",
            "resource_type": "website",
            "project_id": project_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/resources/",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python Resource"


def test_update_resource(client):
    client.post(
        "/auth/register",
        json={
            "username": "updateresource",
            "email": "updateresource@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "updateresource",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Update Resource Project",
            "symbol": "UPRES",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    resource = client.post(
        "/api/resources/",
        json={
            "title": "Old Resource",
            "url": "https://example.com/",
            "description": "Old description",
            "resource_type": "article",
            "project_id": project_id,
        },
        headers=headers,
    )

    resource_id = resource.json()["id"]

    response = client.put(
        f"/api/resources/{resource_id}",
        json={
            "title": "New Resource",
            "url": "https://example.org/",
            "description": "New description",
            "resource_type": "paper",
            "project_id": project_id,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New Resource"
    assert response.json()["url"] == "https://example.org/"
    assert response.json()["resource_type"] == "paper"


def test_delete_resource(client):
    client.post(
        "/auth/register",
        json={
            "username": "deleteresource",
            "email": "deleteresource@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "deleteresource",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = client.post(
        "/api/projects/",
        json={
            "name": "Delete Resource Project",
            "symbol": "DELRES",
            "description": "Test project",
        },
        headers=headers,
    )

    project_id = project.json()["id"]

    resource = client.post(
        "/api/resources/",
        json={
            "title": "Delete Me",
            "url": "https://example.com/",
            "description": "Temporary resource",
            "resource_type": "website",
            "project_id": project_id,
        },
        headers=headers,
    )

    resource_id = resource.json()["id"]

    response = client.delete(
        f"/api/resources/{resource_id}",
        headers=headers,
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/resources/{resource_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_resources_require_authentication(client):
    response = client.get("/api/resources/")

    assert response.status_code == 401