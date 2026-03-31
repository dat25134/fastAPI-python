---
description: Hướng dẫn tạo một Resource mới (Model, Repository, Service, Schema, API)
---

Để tạo một Resource mới (ví dụ `Item`), hãy thực hiện các bước sau:

1. **Định nghĩa Model**:
   - Tạo `app/models/item.py` kế thừa từ `Base`.
   - Đăng ký model trong `app/models/__init__.py`.

2. **Tạo Schame**:
   - Tạo `app/schemas/item.py` với Pydantic (Base, Create, Update, InDB).

3. **Tạo Repository**:
   - Tạo `app/repositories/item_repository.py`.
   - Đăng ký instance trong `app/repositories/__init__.py`.

4. **Tạo Service**:
   - Tạo `app/services/item_service.py` xử lý Business Logic.
   - Đăng ký instance trong `app/services/__init__.py`.

5. **Tạo Router/Endpoint**:
   - Tạo `app/api/v1/endpoints/items.py`.
   - Đăng ký router trong `app/api/v1/api.py`.

6. **Tạo Migration**:
   - Chạy `docker compose exec api alembic revision --autogenerate -m "Add item table"`.
   - Chạy `docker compose exec api alembic upgrade head`.

7. **Kiểm tra**:
   - Kiểm tra Swagger UI tại `/docs`.
