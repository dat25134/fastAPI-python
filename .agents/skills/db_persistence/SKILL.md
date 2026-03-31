---
name: db_persistence
description: Standard for Designing and Implementing Scalable Database Access in SQLAlchemy 2.0.
---

# Skill: Database Persistence
**Domain**: SQLAlchemy, PostgreSQL, Alembic, Repository Pattern.
**When to Use**: When performing CRUD operations, changing table structure, or executing complex SQL queries.

## Key Rules
- **DO**: Always use `AsyncSession` and `AsyncSessionLocal`.
- **DO**: Always use `scalars().first()` or `scalars().all()` instead of legacy syntax.
- **DO**: Always encapsulate query logic in a `Repository` class.
- **DON'T**: Never perform `db.commit()` in a Repository layer (The Service layer decides when to commit).
- **DON'T**: Never use "Lazy Loading" in async objects (`AttributeError`).

## Code Examples

### ✅ Correct Pattern (Async Repository)
```python
class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
```

### ❌ Anti-pattern (Direct query in Controller)
```python
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    # Error: Direct query in Controller makes code hard to test and maintain
    users = await db.execute(select(User)).scalars().all() 
    return users
```

## AI Agent Instructions

### Generate
When a user requests a new table:
1. Create Model file in `app/models/`.
2. Register in `app/models/__init__.py`.
3. Run `alembic revision --autogenerate`.
4. Create corresponding Repository in `app/repositories/`.

### Review
- Check if `Session` (Sync) is being used instead of `AsyncSession`?
- Check if relationships have `lazy="selectin"` or `joinedload`?
- Check if sensitive fields are excluded in Schemas?

### Detect
- Detect `db.add()` without `await db.commit()` in a Service → Flag: "Data not saved".
- Detect N+1 queries → Flag: "Low performance with large datasets".

### Suggest
- Suggest `db.refresh(db_obj)` after commit to fetch auto-generated data (e.g., IDs).

## Common Bugs
- **Bug**: `MissingGreenlet` error.
  - **Fix**: You're accessing a relationship attribute that wasn't loaded. Use `selectinload`.
- **Bug**: `UniqueConstraintViolation`.
  - **Fix**: Check `UserCreate` schema and Service logic to catch duplicates before inserting.

## Performance Notes
- Always use Indexes for fields frequently used in `WHERE` or `ORDER BY`.
- Use `db.execute(text("..."))` for extremely complex SQL that ORM cannot optimize.

## Related Skills
- `api_design`: Provides data for the Router.
- `logic_service`: Orchestrates different Repositories.
