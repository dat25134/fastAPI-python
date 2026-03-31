import pytest

@pytest.fixture
async def superuser_token(client, test_user):
    login_data = {"username": "test@example.com", "password": "testpassword"}
    login_res = await client.post("/api/v1/login/access-token", data=login_data)
    return login_res.json()["access_token"]

@pytest.mark.asyncio
async def test_read_users_protected(client):
    response = await client.get("/api/v1/users/")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers

@pytest.mark.asyncio
async def test_read_users_authorized(client, superuser_token):
    headers = {"Authorization": f"Bearer {superuser_token}"}
    response = await client.get("/api/v1/users/", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) >= 1

@pytest.mark.asyncio
async def test_create_user_authorized(client, superuser_token):
    headers = {"Authorization": f"Bearer {superuser_token}"}
    user_data = {
        "email": "newuser@example.com",
        "password": "newpassword",
        "full_name": "New User",
        "is_active": True,
        "is_superuser": False
    }
    response = await client.post("/api/v1/users/", json=user_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "newuser@example.com"
