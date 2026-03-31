---
name: api_design
description: Standard for Designing and Implementing Enterprise-grade APIs in FastAPI.
---

# Skill: API Design
**Domain**: FastAPI, Pydantic V2, REST, OpenAPI.
**When to Use**: When creating new endpoints, routers, or request/response schemas.

## Key Rules
- **DO**: Always use **Pydantic V2** (`ConfigDict`, `field_validator`).
- **DO**: Use `from app.api import deps` for dependency injection.
- **DO**: Implement **RFC 6750** compliance for unauthorized access (401 + WWW-Authenticate).
- **DON'T**: Never use Pydantic V1 `@validator` or `class Config`.
- **DON'T**: Avoid returning raw models; always use `response_model` or `schemas.response.ResponseSuccess`.

## Code Examples

### ✅ Correct Pattern (Pydantic V2 Schema)
```python
from pydantic import BaseModel, ConfigDict, field_validator

class MySchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        if not v:
            raise ValueError("Name cannot be empty")
        return v
```

### ✅ Correct Pattern (Router registration)
```python
from app.api.v1.endpoints import my_feature
api_router.include_router(my_feature.router, prefix="/feature", tags=["feature"])
```

## AI Agent Instructions

### Generate
1.  Check for `PROJECT_KNOWLEDGE.md` to identify the current stack.
2.  Ensure Pydantic models use V2 syntax.
3.  Register any new router in `app/api/v1/api.py`.

### Review
- Are we using Pydantic V2?
- Is the error code for auth failure 401 (not 403)?
- Are schemas correctly exported in `app/schemas/__init__.py`?
