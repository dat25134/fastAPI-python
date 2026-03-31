---
name: api_design
description: Standard for Designing and Implementing Enterprise-grade APIs in FastAPI.
---

# Skill: API Design
**Domain**: Routing, Request/Response handling, Middlewares, Versioning.
**When to Use**: When adding a new endpoint, changing data input/output logic, or handling cross-cutting concerns.

## Key Rules
- **DO**: Always use `/api/v[N]/...` for routing.
- **DO**: Always use `Standard Success/Error Schema` for responses.
- **DO**: Always separate Router logic (Controller) from Business Logic (Service).
- **DON'T**: Never write SQL queries directly in the router.
- **DON'T**: Never return SQLAlchemy models directly to the client.

## Code Examples

### ✅ Correct Pattern (Standard Success Response)
```python
@router.get("/", response_model=ResponseSuccess[List[User]])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await user_service.get_users(db)
    return ResponseSuccess(data=users)
```

### ❌ Anti-pattern (Returning Model directly)
```python
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    # Error: No response_model, returning legacy SQLAlchemy object directly
    return db.query(UserModel).all() 
```

## AI Agent Instructions

### Generate
When a user requests a new API:
1. Create Router in `api/v1/endpoints/`.
2. Define Request/Response Schemas.
3. Register Router in `api/v1/api.py`.

### Review
- Check if `response_model` is present?
- Check if SQL is being handled directly?
- Check if the endpoint is in the correct version (`/v1`)?

### Detect
- Detect `async def` without `await` → Flag: "Potential Event Loop blocking".
- Detect `HTTPException` directly in a Repository → Flag: "Violation of Layering".

### Suggest
- Suggest creating a `CommonQueryParams` dependency for repeated query parameters.

## Common Bugs
- **Bug**: Forgot to import the router into `api_router`.
  - **Fix**: Check `app/api/v1/api.py`.
- **Bug**: `Validation Error` (Pydantic) mismatch with frontend.
  - **Fix**: Re-check Schema field types (e.g., `int` vs `string`).

## Performance Notes
- Use `APIRouter` with `tags` for better Swagger UI organization.
- Use `skip` and `limit` (Pagination) for large lists.

## Related Skills
- `db_persistence`: Provides data to the Router.
- `logic_service`: The layer the Router delegates work to.
