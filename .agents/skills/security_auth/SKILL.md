---
name: security_auth
description: Standard for Designing and Implementing Enterprise Security in FastAPI.
---

# Skill: Security & Authentication
**Domain**: JWT, OAuth2, Password Hashing, Permissions.
**When to Use**: Khi cần bảo vệ API, xác thực người dùng, hoặc cấp quyền truy cập.

## Key Rules
- **DO**: Luôn sử dụng `Passlib (bcrypt)` để băm mật khẩu.
- **DO**: Luôn trả về JWT với `exp` (Expiry) và `sub` (User ID).
- **DO**: Luôn sử dụng `OAuth2PasswordBearer` để lấy token.
- **DON'T**: Không bao giờ lưu mật khẩu ở dạng plain text.
- **DON'T**: Không bao giờ lưu các thông tin nhạy cảm (như sđt, cccd) và `sub` của JWT.

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
# Lỗi: Cực kỳ nguy hiểm, mọi người có thể đọc mật khẩu nếu DB bị lộ
user = User(email="test@test.com", password="mypassword123") 
```

## AI Agent Instructions

### Generate
Khi user yêu cầu thêm Security:
1. Tạo `app/core/security.py` cho hashing & JWT.
2. Tạo `app/schemas/token.py` cho login response.
3. Tạo `app/api/deps.py` cho `get_current_user` dependency.

### Review
- Check xem mật khẩu đã được băm trước khi lưu chưa?
- Check xem JWT có thời hạn hết hạn (`exp`) không?
- Check xem các API nhạy cảm đã dùng `Depends(get_current_user)` chưa?

### Detect
- Phát hiện việc dùng thuật toán hashing cũ (như MD5) → Flag: "Bảo mật yếu, kiến nghị đổi sang bcrypt".
- Phát hiện việc dùng `settings.SECRET_KEY` mà không có giá trị mặc định an toàn trong `.env` → Flag: "Rủi ro lộ bí mật".

### Suggest
- Gợi ý dùng `OAuth2PasswordRequestForm` cho API login để tương thích tối đa với Swagger UI.

## Common Bugs
- **Bug**: `JWT Decode Error`.
  - **Fix**: Kiểm tra `SECRET_KEY` và `ALGORITHM` có khớp khi encode và decode không.
- **Bug**: Token hết hạn quá nhanh.
  - **Fix**: Check `ACCESS_TOKEN_EXPIRE_MINUTES` trong `.env`.

## Performance Notes
- Hashing là CPU-bound task, nên dùng `run_in_executor` nếu lưu lượng request cực lớn.

## Related Skills
- `api_design`: Cung cấp router cho login.
- `logic_service`: Nơi thực hiện query xác thực thông tin đăng nhập.
