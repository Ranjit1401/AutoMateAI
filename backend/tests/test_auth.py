def test_signup_creates_user_and_session(client):
    response = client.post("/auth/signup", json={"email": "a@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json()["user"]["email"] == "a@example.com"
    assert "automateai_session" in response.cookies


def test_signup_rejects_duplicate_email(client):
    client.post("/auth/signup", json={"email": "a@example.com", "password": "password123"})
    response = client.post("/auth/signup", json={"email": "a@example.com", "password": "password123"})
    assert response.status_code == 409


def test_login_with_wrong_password_fails(client):
    client.post("/auth/signup", json={"email": "a@example.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "a@example.com", "password": "wrong-password"})
    assert response.status_code == 401


def test_login_with_correct_password_succeeds(client):
    client.post("/auth/signup", json={"email": "a@example.com", "password": "password123"})
    client.post("/auth/logout")
    response = client.post("/auth/login", json={"email": "a@example.com", "password": "password123"})
    assert response.status_code == 200


def test_me_requires_authentication(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_logout_clears_session(authed_client):
    assert authed_client.get("/auth/me").status_code == 200
    authed_client.post("/auth/logout")
    assert authed_client.get("/auth/me").status_code == 401


def test_password_over_72_bytes_does_not_crash(client):
    long_password = "a" * 100
    response = client.post("/auth/signup", json={"email": "b@example.com", "password": long_password})
    assert response.status_code == 201
