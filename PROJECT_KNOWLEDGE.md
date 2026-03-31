# Project Knowledge Base: FastAPI Large System

This document serves as a central source of truth for the project's architecture, standards, and historical context to ensure consistency and prevent regression.

## 🏗️ Architecture Overview

The project follows a decoupled **Service/Repository** architecture:
- **API (app/api)**: FastAPI routers and path definitions.
- **Services (app/services)**: Business logic, validation, and orchestration.
- **Repositories (app/repositories)**: Data persistence logic using SQLAlchemy.
- **Models (app/models)**: Declarative SQLAlchemy models.
- **Schemas (app/schemas)**: Pydantic V2 models for request/response validation.

## 🔐 Security & Authentication

- **JWT Flow**:
    - `POST /login/access-token`: Returns Access Token (30m) and Refresh Token (7d).
    - `POST /login/refresh-token`: Rotates access tokens.
- **Password Policy**: Uses `bcrypt==3.2.0` (pinned for `passlib` compatibility).
- **Standards**:
    - Invalid tokens MUST return `401 Unauthorized` with `WWW-Authenticate: Bearer` header.
    - Passwords MUST NEVER be stored in plain text (enforced in `UserRepository`).

## 🧪 Testing Standard

- **Framework**: `pytest` + `pytest-asyncio` + `httpx`.
- **Database**: Uses `sqlite+aiosqlite:///:memory:` for feature tests.
- **Fixtures**:
    - `setup_db`: Function-scoped (resets DB for each test case).
    - `test_user`: Provides a default Superuser for authorized tests.
- **Command**: `docker compose exec api pytest tests/`

## 📘 Development Rules (AI Agent Instructions)

1.  **Pydantic V2**: Use `@field_validator(mode="before")` and `model_config = ConfigDict(...)`. Avoid Pydantic V1 `@validator` or `class Config`.
2.  **Explicit Imports**: Always ensure `models` and `schemas` are imported when used in endpoint decorators or type hints.
3.  **Dependency Injection**: Use `app.api.deps` for all common dependencies like `get_db`.
4.  **Error Handling**: Use the centralized exception handlers in `app.api.exception_handlers`.

## 📦 Key Dependencies

- **FastAPI**: Main web framework.
- **SQLAlchemy 2.0+**: ORM with async support.
- **Pydantic V2**: Data validation.
- **Bcrypt 3.2.0**: Pinned to avoid `ValueError` with `passlib`.
