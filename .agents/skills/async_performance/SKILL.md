---
name: async_performance
description: Standard for Mastering Asynchronous Performance and Caching in FastAPI.
---

# Skill: Async & Performance
**Domain**: Event Loop, Redis, Background Tasks, Connection Pooling.
**When to Use**: Khi hệ thống bị chậm (Latency cao), cần xử lý nhiều connection đồng thời, hoặc tối ưu hóa tốc độ phản hồi.

## Key Rules
- **DO**: Luôn sử dụng `async def` cho các I/O task (API, DB, Redis).
- **DO**: Luôn sử dụng `run_in_executor` cho các CPU-bound task (như hashing, xử lý ảnh).
- **DO**: Luôn thiết lập TTL (TTL) cho mọi key trong Redis.
- **DON'T**: Không bao giờ sử dụng các thư viện đồng bộ (Sync) bên trong hàm `async def` (như `requests`, `time.sleep`).
- **DON'T**: Không bao giờ commit transaction mà không có `await` (`db.commit()` thay vì `await db.commit()`).

## Code Examples

### ✅ Correct Pattern (Non-blocking I/O)
```python
import httpx

async def call_external_api(url: str):
    async with httpx.AsyncClient() as client:
        # Lợi: Không làm treo hệ thống khi chờ kết quả phản hồi
        return await client.get(url) 
```

### ❌ Anti-pattern (Blocking I/O)
```python
import requests

def call_external_api(url: str):
    # Lỗi: Giết chết hiệu năng của toàn bộ FastAPI app
    return requests.get(url) 
```

## AI Agent Instructions

### Generate
Khi user yêu cầu tối ưu hóa:
1. Phân tích các hàm `sync` đang gọi I/O.
2. Chuyển sang `async` (ví dụ: `requests` -> `httpx`).
3. Cấu hình Redis Cache-Aside pattern.

### Review
- Check xem có đang dùng `time.sleep` lồng trong `async def` không?
- Check xem `await` đã được gọi cho mọi IO operation chưa? (Rất hay quên).

### Detect
- Phát hiện việc dùng `await` lồng nhau quá nhiều trong vòng lặp → Flag: "Sử dụng asyncio.gather để song song hóa".
- Phát hiện việc dùng Redis mà xóa cache sai cách → Flag: "Nguy cơ dữ liệu không đồng nhất".

### Suggest
- Gợi ý dùng `BackgroundTasks` cho các hành động không cần phản hồi kết quả cho người dùng ngay lập tức (Xóa file, Gửi log).

## Common Bugs
- **Bug**: `RuntimeError: Task <...> got Future <...> attached to a different loop`.
  - **Fix**: Bạn đang chia sẻ session SQLAlchemy sai giữa các context. Kiểm tra `get_db`.
- **Bug**: Redis chiếm quá nhiều RAM.
  - **Fix**: Bạn chưa đặt TTL. Use `redis.setex(key, time, value)`.

## Performance Notes
- Sử dụng `uvicorn --workers N` để tận dụng đa nhân CPU.
- Luôn kiểm tra N+1 queries ở DB (Skill `db_persistence`).

## Related Skills
- `db_persistence`: Database tối ưu là nền tảng của hiệu năng.
- `api_design`: Caching ở tầng Router.
