---
name: code_quality
description: Standard for Ensuring Maintaining High Quality, Testing, and Logging in FastAPI.
---

# Skill: Code Quality & Assurance
**Domain**: Logging, Testing (Pytest), Code Review, Mypy, Formatting.
**When to Use**: Khi cần viết Test, cấu hình Log cho Production, hoặc kiểm tra chất lượng code trước khi Commit.

## Key Rules
- **DO**: Luôn sử dụng `Pytest` và `Httpx.AsyncClient` cho integration tests.
- **DO**: Luôn sử dụng `Structured JSON Logging` cho các môi trường quan trọng.
- **DO**: Luôn đảm bảo `Type Hints` đầy đủ cho mọi hàm.
- **DON'T**: Không bao giờ bỏ qua Unit Test cho các logic quan trọng của `Service`.
- **DON'T**: Không bao giờ sử dụng `print()` thay thế cho `logging`.

## Code Examples

### ✅ Correct Pattern (Structured Logging)
```python
import logging
import json

def log_event(event: str, data: dict):
    # Lợi: Dễ dàng phân tích bằng ELK/Graylog
    logging.info(json.dumps({"event": event, "data": data}))
```

### ❌ Anti-pattern (Using print)
```python
def process_data(data):
    # Lỗi: Không thể quản lý Log Level, không thể lưu vào file hiệu quả
    print(f"Processing data: {data}") 
```

## AI Agent Instructions

### Generate
Khi user yêu cầu Test hoặc Quality:
1. Tạo thư mục `tests/` và file tương ứng.
2. Viết Test cases bao hàm cả Success và Error scenarios.
3. Cấu hình `logging.conf` hoặc middleware logging.

### Review
- Check xem có `print()` trong code không?
- Check xem các logic Service quan trọng có Tests chưa?
- Check xem Type Hints có bị `Any` quá nhiều không?

### Detect
- Phát hiện các đoạn code quá phức tạp (Cyclomatic Complexity cao) → Flag: "Kiến nghị Refactor thành các hàm nhỏ hơn".

### Suggest
- Gợi ý dùng `Faker` cho việc tạo dữ liệu Test mẫu.

## Common Bugs
- **Bug**: `Test Database` bị lẫn với `Production Database`.
  - **Fix**: Cấu hình `overrides` cho `get_db` trong `conftest.py`.

## Performance Notes
- Hạn chế Log quá nhiều mức `DEBUG` ở môi trường Production.

## Related Skills
- `api_design`: Integration tests cho API.
- `logic_service`: Unit tests cho Business Logic.
