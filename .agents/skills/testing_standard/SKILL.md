---
name: testing_standard
description: Standard for Designing and Implementing Feature & Unit Tests in FastAPI.
---

# Skill: Testing Standard
**Domain**: Pytest, Async Testing, Httpx, Fixtures.
**When to Use**: When adding logic or API endpoints to ensure code quality and prevent regressions.

## Key Rules
- **DO**: Always use `pytest` with `pytest-asyncio`.
- **DO**: Use `httpx.ASGITransport` to test FastAPI apps without a running server.
- **DO**: Create a separate `conftest.py` for global fixtures (DB, Client).
- **DON'T**: Never run tests against a production database.
- **DON'T**: Avoid mocking critical business logic; prefer integration (feature) tests for APIs.

## Code Examples

### ✅ Correct Pattern (Test Client Fixture)
```python
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

### ✅ Correct Pattern (Feature Test)
```python
@pytest.mark.asyncio
async def test_login(client):
    response = await client.post("/api/v1/login/access-token", data={"username": "test@test.com", "password": "password"})
    assert response.status_code == 200
```

## AI Agent Instructions

### Generate
When creating tests:
1.  Check if `tests/` exists.
2.  Add `conftest.py` if missing.
3.  Name files `test_*.py`.
4.  Ensure all API endpoints have at least one test case for success and one for failure.

### Review
- Is there a test for this new feature?
- Does the test handle async properly?
- Are database sessions cleaned up after tests?

## Common Bugs
- **Bug**: `Event loop closed` or `RuntimeError`.
  - **Fix**: Use `@pytest.mark.asyncio` and ensure session isolation.
- **Bug**: Data pollution between tests.
  - **Fix**: Wrap each test in a transaction or reset the DB after each test.
