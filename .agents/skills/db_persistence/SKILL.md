---
name: db_persistence
description: Standard for Designing and Implementing Scalable Database Access in SQLAlchemy 2.0.
---

# Skill: Database Persistence
**Domain**: SQLAlchemy, PostgreSQL, Alembic, Repository Pattern.
**When to Use**: Khi cần thao tác CRUD, thay đổi cấu trúc bảng, hoặc thực thi các câu lệnh SQL phức tạp.

## Key Rules
- **DO**: Luôn sử dụng `AsyncSession` và `AsyncSessionLocal`.
- **DO**: Luôn sử dụng `scalars().first()` hoặc `scalars().all()` thay vì legacy syntax.
- **DO**: Luôn bọc logic query trong lớp `Repository`.
- **DON'T**: Không bao giờ thực hiện `db.commit()` trong lớp Repository (Lớp Service sẽ quyết định khi nào commit).
- **DON'T**: Không bao giờ sử dụng "Lazy Loading" trong các object async (`AttributeError`).

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
    # Lỗi: Logic gõ trực tiếp query ở Controller làm code khó test
    users = await db.execute(select(User)).scalars().all() 
    return users
```

## AI Agent Instructions

### Generate
Khi user yêu cầu thêm bảng mới:
1. Tạo Model file trong `app/models/`.
2. Đăng ký trong `app/models/__init__.py`.
3. Chạy `alembic revision --autogenerate`.
4. Tạo Repository tương ứng trong `app/repositories/`.

### Review
- Check xem có đang dùng `Session` (Sync) thay vì `AsyncSession` không?
- Check xem các quan hệ (`relationship`) đã có `lazy="selectin"` hoặc `joinedload` chưa?
- Check xem các trường nhạy cảm có bị bỏ qua (`exclude`) trong Schema không?

### Detect
- Phát hiện việc dùng `db.add()` mà không có `await db.commit()` trong Service → Flag: "Dữ liệu chưa được lưu".
- Phát hiện các query N+1 → Flag: "Hiệu năng thấp khi dữ liệu lớn".

### Suggest
- Gợi ý dùng `db.refresh(db_obj)` sau khi commit để lấy dữ liệu mới nhất (như ID tự sinh).

## Common Bugs
- **Bug**: `MissingGreenlet` error.
  - **Fix**: Bạn đang truy cập một thuộc tính relationship chưa được load. Use `selectinload`.
- **Bug**: `UniqueConstraintViolation`.
  - **Fix**: Check `UserCreate` schema và Service logic để bắt lỗi trùng lặp trước khi insert.

## Performance Notes
- Luôn sử dụng Index cho các trường thường xuyên `WHERE` hoặc `ORDER BY`.
- Sử dụng `db.execute(text("..."))` cho các câu SQL cực kỳ phức tạp mà ORM không tối ưu được.

## Related Skills
- `api_design`: Cung cấp dữ liệu cho Router.
- `logic_service`: Nơi điều phối các Repo.
