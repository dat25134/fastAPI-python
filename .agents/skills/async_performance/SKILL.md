---
name: async_performance
description: Standard for Mastering Asynchronous Performance and Caching in FastAPI.
---

# Skill: Async & Performance
**Domain**: Event Loop, Redis, Background Tasks, Connection Pooling.
**When to Use**: When the system is slow (high latency), needs to handle many simultaneous connections, or optimize response speed.

## Key Rules
- **DO**: Always use `async def` for I/O tasks (API, DB, Redis).
- **DO**: Always use `run_in_executor` for CPU-bound tasks (e.g., hashing, image processing).
- **DO**: Always set TTL for every key in Redis.
- **DON'T**: Never use synchronous (Sync) libraries within an `async def` function (e.g., `requests`, `time.sleep`).
- **DON'T**: Never commit a transaction without `await` (`db.commit()` instead of `await db.commit()`).

## Code Examples

### ✅ Correct Pattern (Non-blocking I/O)
```python
import httpx

async def call_external_api(url: str):
    async with httpx.AsyncClient() as client:
        # Advantage: Does not block the system while waiting for the result
        return await client.get(url) 
```

### ❌ Anti-pattern (Blocking I/O)
```python
import requests

def call_external_api(url: str):
    # Error: Kills the performance of the entire FastAPI app
    return requests.get(url) 
```

## AI Agent Instructions

### Generate
When a user requests optimization:
1. Analyze `sync` functions calling I/O.
2. Switch to `async` (e.g., `requests` -> `httpx`).
3. Configure Redis Cache-Aside pattern.

### Review
- Check if `time.sleep` is nested within `async def`?
- Check if `await` is called for every IO operation? (Easy to forget).

### Detect
- Detect nested `await` too many times in a loop → Flag: "Use asyncio.gather to parallelize".
- Detect using Redis and deleting cache incorrectly → Flag: "Risk of data inconsistency".

### Suggest
- Suggest using `BackgroundTasks` for actions that don't need to return results to the user immediately (Delete files, Send logs).

## Common Bugs
- **Bug**: `RuntimeError: Task <...> got Future <...> attached to a different loop`.
  - **Fix**: You are sharing SQLAlchemy session incorrectly between contexts. Check `get_db`.
- **Bug**: Redis consumes too much RAM.
  - **Fix**: You haven't set TTL. Use `redis.setex(key, time, value)`.

## Performance Notes
- Use `uvicorn --workers N` to leverage multi-core CPUs.
- Always check N+1 queries in DB (Skill `db_persistence`).

## Related Skills
- `db_persistence`: Optimized Database is the foundation of performance.
- `api_design`: Caching at the Router layer.
