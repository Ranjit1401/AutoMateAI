def test_tasks_list_starts_empty(authed_client):
    response = authed_client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_memory_create_and_list(authed_client):
    created = authed_client.post("/memory", json={"content": "Vegetarian", "category": "dietary"})
    assert created.status_code == 201

    listed = authed_client.get("/memory")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["content"] == "Vegetarian"


def test_memory_delete(authed_client):
    created = authed_client.post("/memory", json={"content": "Vegetarian"})
    memory_id = created.json()["id"]

    deleted = authed_client.delete(f"/memory/{memory_id}")
    assert deleted.status_code == 204
    assert authed_client.get("/memory").json() == []


def test_memory_delete_nonexistent_returns_404(authed_client):
    response = authed_client.delete("/memory/does-not-exist")
    assert response.status_code == 404


def test_logs_endpoint_requires_auth(client):
    assert client.get("/logs").status_code == 401


def test_preferences_default_and_update(authed_client):
    defaults = authed_client.get("/settings/preferences")
    assert defaults.status_code == 200
    assert defaults.json()["theme"] == "dark"

    updated = authed_client.put("/settings/preferences", json={"theme": "light"})
    assert updated.status_code == 200
    assert updated.json()["theme"] == "light"
