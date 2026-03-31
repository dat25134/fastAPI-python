---
name: api_design
description: Standard for Designing and Implementing Enterprise-grade APIs in FastAPI.
---

# Skill: API Design
**Domain**: Routing, Request/Response handling, Middlewares, Versioning.
**When to Use**: Khi cần thêm Endpoint mới, thay đổi logic nhận dữ liệu từ request, hoặc xử lý các vấn đề xuyên suốt (cross-cutting concerns).

## Key Rules
- **DO**: Luôn sử dụng `/api/v[N]/...` cho routing.
- **DO**: Luôn sử dụng `Standard Success/Error Schema` cho response.
- **DO**: Luôn tách biệt Logic Router (Controller) và Logic Nghiệp vụ (Service).
- **DON'T**: Không bao giờ viết SQL query trực tiếp trong router.
- **DON'T**: Không bao giờ trả về SQLAlchemy Model trực tiếp cho client.

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
    # Lỗi: Không có response_model, trả về trực tiếp SQLAlchemy object
    return db.query(UserModel).all() 
```

## AI Agent Instructions

### Generate
Khi user yêu cầu tạo API mới:
1. Tạo Router trong `api/v1/endpoints/`.
2. Định nghĩa Request/Response Schema.
3. Đăng ký Router trong `api/v1/api.py`.

### Review
- Check xem có `response_model` chưa?
- Check xem có đang xử lý SQL trực tiếp không?
- Check xem endpoint có nằm đúng version (`/v1`) không?

### Detect
- Phát hiện các hàm `async def` mà không có `await` → Flag: "Tiềm năng chặn Event Loop".
- Phát hiện việc dùng `HTTPException` trực tiếp trong Repository → Flag: "Vi phạm Layering".

### Suggest
- Khi thấy tham số query lặp lại nhiều lần → Gợi ý tạo `CommonQueryParams` dependency.

## Common Bugs
- **Bug**: Quên import router vào `api_router`.
  - **Fix**: Check `app/api/v1/api.py`.
- **Bug**: `Validation Error` (Pydantic) không khớp với frontend.
  - **Fix**: Check lại Schema field types (ví dụ: `int` vs `string`).

## Performance Notes
- Sử dụng `APIRouter` với `tags` để Swagger UI được tổ chức tốt hơn.
- Trả về danh sách lớn nên có `skip` và `limit` (Pagination).

## Related Skills
- `db_persistence`: Cần repo để lấy dữ liệu.
- `logic_service`: Nơi Router ủy thác công việc.
