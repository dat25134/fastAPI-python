---
name: code_quality
description: Standard for Ensuring Maintaining High Quality, Testing, and Logging in FastAPI.
---

# Skill: Code Quality & Assurance
**Domain**: Logging, Testing (Pytest), Code Review, Mypy, Formatting.
**When to Use**: When writing tests, configuring logs for Production, or verifying code quality before committing.

## Key Rules
- **DO**: Always use `Pytest` and `Httpx.AsyncClient` for integration tests.
- **DO**: Always use `Structured JSON Logging` for critical environments.
- **DO**: Always ensure full `Type Hints` for every function.
- **DON'T**: Never skip Unit Tests for critical `Service` logic.
- **DON'T**: Never use `print()` as a replacement for `logging`.

## Code Examples

### ✅ Correct Pattern (Structured Logging)
```python
import logging
import json

def log_event(event: str, data: dict):
    # Benefit: Easy analysis with ELK/Graylog
    logging.info(json.dumps({"event": event, "data": data}))
```

### ❌ Anti-pattern (Using print)
```python
def process_data(data):
    # Error: Cannot manage Log Level, cannot save to files effectively
    print(f"Processing data: {data}") 
```

## AI Agent Instructions

### Generate
When a user requests Testing or Quality:
1. Create a `tests/` directory and corresponding file.
2. Write Test cases covering both Success and Error scenarios.
3. Configure `logging.conf` or logging middleware.

### Review
- Check if `print()` exists in the code?
- Check if critical Service logic has Tests?
- Check if Type Hints are used correctly (avoid `Any`)?

### Detect
- Detect overly complex code (High Cyclomatic Complexity) → Flag: "Recommend refactoring into smaller functions".

### Suggest
- Suggest using `Faker` for generating sample Test data.

## Common Bugs
- **Bug**: `Test Database` mixed with `Production Database`.
  - **Fix**: Configure `overrides` for `get_db` in `conftest.py`.

## Performance Notes
- Minimize `DEBUG` level Logs in Production environments.

## Related Skills
- `api_design`: Integration tests for APIs.
- `logic_service`: Unit tests for Business Logic.
