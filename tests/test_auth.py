
import pytest
from app.core import security

@pytest.mark.asyncio
async def test_login_access_token(client, test_user):
    login_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }
    response = await client.post("/api/v1/login/access-token", data=login_data)
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert "refresh_token" in content
    assert content["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid(client):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = await client.post("/api/v1/login/access-token", data=login_data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_read_user_me(client, test_user):
    # Get token
    login_data = {"username": "test@example.com", "password": "testpassword"}
    login_res = await client.post("/api/v1/login/access-token", data=login_data)
    token = login_res.json()["access_token"]
    
    # Use token
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_refresh_token(client, test_user):
    # Get token
    login_data = {"username": "test@example.com", "password": "testpassword"}
    login_res = await client.post("/api/v1/login/access-token", data=login_data)
    refresh_token = login_res.json()["refresh_token"]
    
    # Refresh
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = await client.post("/api/v1/login/refresh-token", headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
