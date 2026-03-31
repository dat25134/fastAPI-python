---
name: logic_service
description: Standard for Designing and Implementing Business Logic in the Service Layer.
---

# Skill: Logic & Service Layer
**Domain**: Business Rules, Dependency Coordination, Service Injection.
**When to Use**: When performing logic calculations, orchestrating multiple repos, or calling 3rd party APIs.

## Key Rules
- **DO**: Always encapsulate repositories within a `Service` class.
- **DO**: Always handle check logic (Existence, Permission) at this layer.
- **DO**: Be responsible for `db.commit()` and `db.rollback()`.
- **DON'T**: Never expose SQLAlchemy models to the Controller (Controller only receives schemas).
- **DON'T**: Never write business logic in a Repository.

## Code Examples

### ✅ Correct Pattern (Service Orchestration)
```python
class UserService:
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        user = await user_repository.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        db_obj = await user_repository.create(db, obj_in=user_in)
        await db.commit() 
        return db_obj
```

### ❌ Anti-pattern (Logic in Controller)
```python
@router.post("/")
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Error: User existence check logic in Controller makes code hard to maintain
    user = await db.execute(select(User).filter(User.email == user_in.email))
    if user.scalars().first():
         raise HTTPException(status_code=400, detail="User exists")
    ...
```

## AI Agent Instructions

### Generate
When a user requests a new business logic:
1. Create a file in `app/services/`.
2. Define the handling function with `AsyncSession` and `Schemas` as parameters.
3. Register the instance in `app/services/__init__.py`.

### Review
- Check if the Service layer performs `db.commit()`?
- Check if check logic (e.g., "User exists?") is done before insertion?

### Detect
- Detect `db.query()` in a Service → Flag: "Use Repository instead".
- Detect Controller calling Repository directly → Flag: "Violation of Service Layering".

### Suggest
- Suggest using `db.begin()` if the logic includes complex steps requiring high transaction atomicity.

## Common Bugs
- **Bug**: `IntegrityError` when saving data.
  - **Fix**: You haven't checked input data (e.g., Duplicate email).
- **Bug**: Data not saved.
  - **Fix**: Check if `await db.commit()` has been called.

## Performance Notes
- Minimize repo calls within a Service loop. Optimize repo query to fetch large data at once.

## Related Skills
- `db_persistence`: Provides basic CRUD functions.
- `api_design`: Calls Service to handle Request.
