---
name: security_auth
description: Standard for Designing and Implementing Enterprise Security in FastAPI.
---

# Skill: Security & Authentication
**Domain**: JWT, OAuth2, Password Hashing, Permissions.
**When to Use**: When protecting the API, authenticating users, or granting access permissions.

## Key Rules
- **DO**: Always use `Passlib (bcrypt)` for password hashing.
- **DO**: Always return JWT with `exp` (Expiry) and `sub` (User ID).
- **DO**: Always use `OAuth2PasswordBearer` to retrieve the token.
- **DON'T**: Never store passwords in plain text.
- **DON'T**: Never store sensitive information (e.g., ID numbers) in the JWT `sub`.

## Code Examples

### ✅ Correct Pattern (Password Hashing)
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)
```

### ❌ Anti-pattern (Saving Plain Text)
```python
# Error: Extremely dangerous, anyone can read passwords if DB is leaked
user = User(email="test@test.com", password="mypassword123") 
```

## AI Agent Instructions

### Generate
When a user requests adding Security:
1. Create `app/core/security.py` for hashing & JWT.
2. Create `app/schemas/token.py` for login response.
3. Create `app/api/deps.py` for `get_current_user` dependency.

### Review
- Check if password has been hashed before saving?
- Check if JWT has an expiration time (`exp`)?
- Check if sensitive APIs use `Depends(get_current_user)`?

### Detect
- Detect use of legacy hashing algorithms (like MD5) → Flag: "Weak security, recommend changing to bcrypt".
- Detect using `settings.SECRET_KEY` without a secure default value in `.env` → Flag: "Risk of secret leakage".

### Suggest
- Suggest using `OAuth2PasswordRequestForm` for login API to ensure maximum compatibility with Swagger UI.

## Common Bugs
- **Bug**: `JWT Decode Error`.
  - **Fix**: Check if `SECRET_KEY` and `ALGORITHM` match during encode and decode.
- **Bug**: Token expires too quickly.
  - **Fix**: Check `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`.

## Performance Notes
- Hashing is a CPU-bound task, should use `run_in_executor` if request volume is extremely large.

## Related Skills
- `api_design`: Provides router for login.
- `logic_service`: Performs queries to authenticate login information.
