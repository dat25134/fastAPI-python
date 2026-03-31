---
description: Step-by-step guide to create a new Resource (Model, Repository, Service, Schema, API)
---

To create a new Resource (e.g., `Item`), follow these steps:

1. **Define the Model**:
   - Create `app/models/item.py` inheriting from `Base`.
   - Register the model in `app/models/__init__.py`.

2. **Create Schemas**:
   - Create `app/schemas/item.py` with Pydantic models (Base, Create, Update, Response).

3. **Create Repository**:
   - Create `app/repositories/item_repository.py`.
   - Register the singleton instance in `app/repositories/__init__.py`.

4. **Create Service**:
   - Create `app/services/item_service.py` to handle Business Logic.
   - Register the singleton instance in `app/services/__init__.py`.

5. **Create Router/Endpoint**:
   - Create `app/api/v1/endpoints/items.py`.
   - Register the router in `app/api/v1/api.py`.

6. **Run Migration**:
   - Run `docker compose exec api alembic revision --autogenerate -m "Add item table"`.
   - Run `docker compose exec api alembic upgrade head`.

7. **Verify**:
   - Check Swagger UI at `/docs`.
