---
name: logic_service
description: Standard for Designing and Implementing Business Logic in the Service Layer.
---

# Skill: Logic & Service Layer
**Domain**: Business Rules, Dependency Coordination, Service Injection.
**When to Use**: Khi cần thực hiện các phép tính logic, điều phối nhiều repos, hoặc gọi API bên thứ 3.

## Key Rules
- **DO**: Luôn bọc các repository vào lớp `Service`.
- **DO**: Luôn xử lý logic kiểm tra (Existence, Permission) ở tầng này.
- **DO**: Chịu trách nhiệm thực hiện `db.commit()` và `db.rollback()`.
- **DON'T**: Không bao giờ lộ các model SQLAlchemy sang Controller (Controller chỉ nhận schemas).
- **DON'T**: Không bao giờ viết logic nghiệp vụ trong Repository.

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
    # Lỗi: Logic kiểm tra người dùng tồn tại nằm ở Controller làm code khó bảo trì
    user = await db.execute(select(User).filter(User.email == user_in.email))
    if user.scalars().first():
         raise HTTPException(status_code=400, detail="User exists")
    ...
```

## AI Agent Instructions

### Generate
Khi user yêu cầu thêm logic nghiệp vụ mới:
1. Tạo file trong `app/services/`.
2. Định nghĩa hàm xử lý với các tham số là `AsyncSession` và `Schemas`.
3. Đăng ký instance trong `app/services/__init__.py`.

### Review
- Check xem tầng Service có thực hiện `db.commit()` chưa?
- Check xem logic kiểm tra (như "User exists?") đã được thực hiện trước khi insert chưa?

### Detect
- Phát hiện việc dùng `db.query()` trong Service → Flag: "Sử dụng Repository thay thế".
- Phát hiện Controller gọi trực tiếp Repository → Flag: "Vi phạm Service Layering".

### Suggest
- Gợi ý dùng `db.begin()` nếu logic bao gồm nhiều bước phức tạp cần Transaction tính nguyên tử cao.

## Common Bugs
- **Bug**: `IntegrityError` khi lưu dữ liệu.
  - **Fix**: Bạn chưa kiểm tra dữ liệu đầu vào (Ví dụ: Email trùng).
- **Bug**: Dữ liệu không được lưu.
  - **Fix**: Kiểm tra xem `await db.commit()` đã được gọi chưa.

## Performance Notes
- Hạn chế các vòng lặp gọi Repo trong Service. Nên tối ưu query Repo trả về một lần dữ liệu lớn.

## Related Skills
- `db_persistence`: Cung cấp các hàm CRUD cơ bản.
- `api_design`: Gọi Service để xử lý Request.
