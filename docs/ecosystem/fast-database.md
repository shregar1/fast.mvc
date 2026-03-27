# 🗄️ FastDatabase

**Shared SQLAlchemy ORM models, Repositories, and Production Patterns.**

FastDatabase is the persistence layer of the FastMVC ecosystem. It ships with a library of declarative models, mixins, and repository logic to handle anything from users and auth to commerce and audit logs.

---

## 🏗️ Core Mixins

FastDatabase provides standardized mixins for common production patterns:

| Mixin | Role | Description |
|-------|------|-------------|
| **`UUIDPrimaryKeyMixin`** | **Identities** | Uses UUIDs to prevent ID enumeration. |
| **`TimestampMixin`** | **Audit** | Automatic `created_at` & `updated_at`. |
| **`SoftDeleteMixin`** | **Safety** | Logical deletion (`is_deleted=True`) and filtering logic. |
| **`OrganizationScopedMixin`** | **SaaS** | Multi-tenancy scoping via `organization_id`. |
| **`OptimisticLockMixin`** | **Concurrency** | Version-based locking (`version` column) for safe updates. |
| **`AuditActorMixin`** | **Compliance** | Tracks `created_by_id` and `updated_by_id` FKs to `user.id`. |

---

## 📦 Baked-in Models

FastDatabase includes production-replicated tables for core business entities:
- **Identity:** `User`, `UserOneTimeToken`, `UserLoginEvent`, `UserMfaFactor`.
- **SaaS:** `Organization`, `Subscription`, `Plan`.
- **Commerce:** `Order`, `Invoice`, `Cart`, `Payment`.
- **System:** `SystemSetting`, `SecurityEvent`, `AuditLog`.

---

## 🛠️ Repository Pattern

The `fast_database.repositories` submodule provides a base `IRepository` and `FilterOperator` for clean data access:

```python
from fast_database.repositories.user import UserRepository

# Filter with operators
repo = UserRepository(session)
users = repo.find_all(filters=[("email", FilterOperator.ILIKE, "%@fastmvc.com")])
```

---

## 🚀 Migrations & Best Practices

FastDatabase is designed to be used with **Alembic**.

### `Alembic Autogenerate`
To use FastDatabase models with Alembic, ensure your `env.py` registers the models:
```python
import fast_database.models  # Registers all tables on Base.metadata
from fast_database.models import Base

target_metadata = Base.metadata
```

Apply migrations:
```bash
alembic revision --autogenerate -m "Add custom table"
alembic upgrade head
```

---

## 🛠️ Installation

FastDatabase can be installed in any SQLAlchemy project:
```bash
pip install fast-database
```
Add **`[dev]`** to include `factory-boy` for testing.
