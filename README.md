<div align="center">

# 🚀 FastMVC

### Production-Ready MVC Framework for FastAPI

[![PyPI version](https://img.shields.io/pypi/v/pyfastmvc.svg?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/pyfastmvc/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Build enterprise-grade APIs in minutes, not hours.**

[Installation](#-installation) •
[Quick Start](#-quick-start) •
[Features](#-features) •
[Documentation](#-documentation) •
[Contributing](#-contributing)

---

</div>

## 🎯 Why FastMVC?

| Pain Point | FastMVC Solution |
|------------|------------------|
| 🏗️ **Project Setup Takes Hours** | One command generates a complete project structure |
| 📁 **Inconsistent Code Organization** | Enforced MVC pattern with clear separation of concerns |
| 🔐 **Security is an Afterthought** | JWT, rate limiting, and security headers built-in |
| 🗄️ **Database Migrations are Complex** | Simple `fastmvc migrate` commands |
| ✏️ **Writing CRUD is Repetitive** | Auto-generate entities with full CRUD scaffolding |
| 🧪 **Testing Setup is Tedious** | Pre-configured pytest with fixtures included |
| 🛡️ **Middleware is Scattered** | [90+ production-ready middlewares](https://pypi.org/project/fastmvc-middleware/) included |

---

## 📦 Installation

### Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a blazing fast Python package manager:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install FastMVC
uv pip install pyfastmvc
```

### Using pip

```bash
pip install pyfastmvc
```

Verify installation:

```bash
fastmvc --version
# → fastmvc, version 1.2.0
```

---

## ⚡ Quick Start

### 1️⃣ Create a New Project

```bash
fastmvc generate my_api
```

### 2️⃣ Setup & Run

```bash
cd my_api

# Using uv (recommended)
uv sync
uv run fastmvc migrate upgrade
uv run uvicorn app:app --reload

# Or using pip
pip install -r requirements.txt
cp .env.example .env
docker-compose up -d          # Start PostgreSQL + Redis
fastmvc migrate upgrade       # Run migrations
python -m uvicorn app:app --reload
```

### 3️⃣ Done! 🎉

Your API is running at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Optional FastMVC packages

Generated projects depend on **fastmvc_core** by default. You can add optional features by installing extra packages:

| Package | Description |
|--------|-------------|
| **fastmvc_dashboards** | Health, API, queues, tenants, secrets, and workflows dashboards |
| **fastmvc_channels** | Real-time WebSocket channels hub (Redis/Kafka backends) |
| **fastmvc_notifications** | Notifications service (long-poll, SSE) |
| **fastmvc_kafka** | Kafka producer, consumer, and worker |
| **fastmvc_webrtc** | WebRTC signaling service |

Install only what you need:

```bash
pip install fastmvc_dashboards fastmvc_channels
# or install all optional deps
pip install -r requirements-optional.txt
```

The app wires these routers only when the corresponding package is installed, so a minimal project with just **fastmvc_core** runs without them.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🏗️ MVC Architecture
Clean separation with Controllers, Services, and Repositories

```python
# controllers/user/login.py
class UserLoginController(IController):
    async def post(self, request: LoginDTO):
        return await self.service.run(request)
```

</td>
<td width="50%">

### ⚡ CLI Scaffolding
Generate complete CRUD in seconds

```bash
fastmvc add entity Product
# Creates: model, repo, service,
# controller, DTOs, and tests!
```

</td>
</tr>
<tr>
<td width="50%">

### 🔐 Security Built-In
JWT auth, rate limiting, security headers

```python
# Automatic JWT protection
@router.post("/protected")
async def secure_endpoint(
    user: User = Depends(get_current_user)
):
    return {"user": user.email}
```

</td>
<td width="50%">

### 💾 Smart Caching
Redis caching with decorators

```python
@cache.cached(ttl=300, prefix="user")
async def get_user(user_id: int):
    return await db.fetch_user(user_id)
```

</td>
</tr>
<tr>
<td width="50%">

### 🗄️ Easy Migrations
Alembic migrations simplified

```bash
fastmvc migrate generate "add products"
fastmvc migrate upgrade
fastmvc migrate status
```

</td>
<td width="50%">

### 📝 Type Safety
Full Pydantic v2 validation

```python
class UserDTO(BaseRequestDTO):
    email: EmailStr
    password: str = Field(min_length=8)
```

</td>
</tr>
</table>

---

## 🛠️ CLI Commands

### Project Management

```bash
# Create a new project
fastmvc generate my_project

# With all options
fastmvc generate my_project \
    --output-dir ~/projects \
    --git \      # Initialize git repo
    --venv \     # Create virtual environment
    --install    # Install dependencies
```

### Entity Generation

```bash
# Generate complete CRUD for an entity
fastmvc add entity Product
```

This creates:
```
📁 Generated Files:
├── models/product.py           # SQLAlchemy model
├── repositories/product.py     # Data access layer
├── services/product/           # Business logic
│   ├── abstraction.py
│   └── crud.py
├── controllers/product/        # API endpoints
├── dtos/requests/product/      # Request DTOs
│   ├── create.py
│   └── update.py
└── tests/unit/.../test_product.py
```

### Database Migrations

```bash
fastmvc migrate generate "add product table"  # Create migration
fastmvc migrate upgrade                        # Apply migrations
fastmvc migrate downgrade                      # Rollback one step
fastmvc migrate status                         # Show current status
fastmvc migrate history                        # Show all migrations
```

---

## 🏛️ Architecture Overview

FastMVC implements a clean **Model-View-Controller (MVC)** pattern optimized for APIs:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🌐 CLIENT                                              │
│                          (Browser, Mobile App, API Consumer)                              │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           │ HTTP/HTTPS
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ⚡ FASTAPI APPLICATION                                    │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                            🛡️ MIDDLEWARE PIPELINE                                   │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │  │
│  │  │ Request  │→│  Timing  │→│  Rate    │→│   JWT    │→│ Logging  │→│   Security   │ │  │
│  │  │ Context  │ │          │ │  Limit   │ │   Auth   │ │          │ │   Headers    │ │  │
│  │  │ (URN)    │ │ (Perf)   │ │ (Abuse)  │ │ (Token)  │ │ (Audit)  │ │ (CSP/HSTS)   │ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│                                           │                                               │
│                                           ▼                                               │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              🎮 CONTROLLER LAYER                                    │  │
│  │                                                                                     │  │
│  │   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐                  │  │
│  │   │  UserLogin      │   │  UserRegister   │   │  ProductCRUD    │   ...            │  │
│  │   │  Controller     │   │  Controller     │   │  Controller     │                  │  │
│  │   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘                  │  │
│  │            │ Validate & Route    │                     │                           │  │
│  └────────────┼─────────────────────┼─────────────────────┼───────────────────────────┘  │
│               │                     │                     │                               │
│               ▼                     ▼                     ▼                               │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                               🔧 SERVICE LAYER                                      │  │
│  │                           (Business Logic & Rules)                                  │  │
│  │                                                                                     │  │
│  │   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐                  │  │
│  │   │  UserLogin      │   │ UserRegistration│   │  ProductCRUD    │   ...            │  │
│  │   │  Service        │   │  Service        │   │  Service        │                  │  │
│  │   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘                  │  │
│  │            │ Business Logic      │                     │                           │  │
│  └────────────┼─────────────────────┼─────────────────────┼───────────────────────────┘  │
│               │                     │                     │                               │
│               ▼                     ▼                     ▼                               │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              🗄️ REPOSITORY LAYER                                    │  │
│  │                            (Data Access Abstraction)                                │  │
│  │                                                                                     │  │
│  │   ┌─────────────────┐   ┌─────────────────────────────────────────────────────┐    │  │
│  │   │ UserRepository  │   │              IRepository (Base)                     │    │  │
│  │   │                 │   │  • retrieve_record_by_filter(filters, operators)    │    │  │
│  │   │ • find_by_email │   │  • create_record(data)                              │    │  │
│  │   │ • check_login   │   │  • update_record_by_filter(filters, data)           │    │  │
│  │   │ • update_status │   │  • delete_record_by_filter(filters)                 │    │  │
│  │   └────────┬────────┘   │  • count_by_filter(filters)                         │    │  │
│  │            │            │  • exists_by_filter(filters)                        │    │  │
│  │            │            └─────────────────────────────────────────────────────┘    │  │
│  └────────────┼───────────────────────────────────────────────────────────────────────┘  │
│               │                                                                           │
└───────────────┼───────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                  💾 DATA LAYER                                            │
│                                                                                           │
│   ┌─────────────────────────────────┐       ┌─────────────────────────────────┐          │
│   │        🐘 PostgreSQL            │       │          🔴 Redis               │          │
│   │                                 │       │                                 │          │
│   │  ┌───────────┐ ┌───────────┐   │       │  ┌───────────┐ ┌───────────┐   │          │
│   │  │   users   │ │ products  │   │       │  │  Session  │ │   Cache   │   │          │
│   │  │   table   │ │   table   │   │       │  │   Store   │ │   Store   │   │          │
│   │  └───────────┘ └───────────┘   │       │  └───────────┘ └───────────┘   │          │
│   │                                 │       │                                 │          │
│   │  SQLAlchemy ORM + Alembic      │       │  Rate Limit + Caching          │          │
│   └─────────────────────────────────┘       └─────────────────────────────────┘          │
│                                                                                           │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Lifecycle

### Complete Request → Response Flow

```
 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                              📥 INCOMING REQUEST                                     │
 │                         POST /user/login { email, password }                         │
 └─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
      ┌───────────────────────────────────┼───────────────────────────────────┐
      │                                   ▼                                   │
      │  ╔═══════════════════════════════════════════════════════════════╗   │
      │  ║              1️⃣  REQUEST CONTEXT MIDDLEWARE                    ║   │
      │  ╠═══════════════════════════════════════════════════════════════╣   │
      │  ║  • Generate unique URN: 01ARZ3NDEKTSV4RRFFQ69G5FAV            ║   │
      │  ║  • Record start timestamp                                      ║   │
      │  ║  • Attach to request.state for tracing                        ║   │
      │  ╚═══════════════════════════════════════════════════════════════╝   │
      │                                   │                                   │
      │                                   ▼                                   │
      │  ╔═══════════════════════════════════════════════════════════════╗   │
      │  ║              2️⃣  TIMING MIDDLEWARE                             ║   │
      │  ╠═══════════════════════════════════════════════════════════════╣   │
      │  ║  • Start performance timer                                     ║   │
      │  ║  • Will add X-Process-Time header on response                 ║   │
      │  ╚═══════════════════════════════════════════════════════════════╝   │
      │                                   │                                   │
      │                                   ▼                                   │
      │  ╔═══════════════════════════════════════════════════════════════╗   │
      │  ║              3️⃣  RATE LIMIT MIDDLEWARE                         ║   │
      │  ╠═══════════════════════════════════════════════════════════════╣   │
      │  ║  • Check sliding window: 60 req/min, 1000 req/hour            ║   │
      │  ║  • If exceeded → 429 Too Many Requests                        ║   │
      │  ║  • Add headers: X-RateLimit-Remaining, Retry-After            ║   │
      │  ╚═══════════════════════════════════════════════════════════════╝   │
      │                                   │                                   │
      │                                   ▼                                   │
      │  ╔═══════════════════════════════════════════════════════════════╗   │
      │  ║              4️⃣  AUTHENTICATION MIDDLEWARE                     ║   │
      │  ╠═══════════════════════════════════════════════════════════════╣   │
      │  ║  • Check if route is protected                                 ║   │
      │  ║  • /user/login is UNPROTECTED → skip JWT validation           ║   │
      │  ║  • Protected routes: validate JWT, check user session         ║   │
      │  ╚═══════════════════════════════════════════════════════════════╝   │
      │                                   │                                   │
  M   │                                   ▼                                   │
  I   │  ╔═══════════════════════════════════════════════════════════════╗   │
  D   │  ║              5️⃣  LOGGING MIDDLEWARE                            ║   │
  D   │  ╠═══════════════════════════════════════════════════════════════╣   │
  L   │  ║  • Log: method, path, client IP, user agent                   ║   │
  E   │  ║  • Structured JSON logging for observability                  ║   │
  W   │  ╚═══════════════════════════════════════════════════════════════╝   │
  A   │                                   │                                   │
  R   │                                   ▼                                   │
  E   │  ╔═══════════════════════════════════════════════════════════════╗   │
      │  ║              6️⃣  CORS & SECURITY HEADERS                       ║   │
      │  ╠═══════════════════════════════════════════════════════════════╣   │
      │  ║  • CORS: Allow-Origin, Allow-Methods, Allow-Headers           ║   │
      │  ║  • HSTS: Strict-Transport-Security                            ║   │
      │  ║  • CSP: Content-Security-Policy                               ║   │
      │  ║  • X-Frame-Options, X-Content-Type-Options                    ║   │
      │  ╚═══════════════════════════════════════════════════════════════╝   │
      │                                   │                                   │
      └───────────────────────────────────┼───────────────────────────────────┘
                                          │
                                          ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                           🎮 CONTROLLER: UserLoginController                         │
 ├─────────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                      │
 │   async def post(self, request: UserLoginRequestDTO):                               │
 │       ┌──────────────────────────────────────────────────────────────────┐          │
 │       │  1. Validate request payload (Pydantic v2)                       │          │
 │       │     • email: EmailStr ✓                                          │          │
 │       │     • password: str (min 8 chars) ✓                              │          │
 │       ├──────────────────────────────────────────────────────────────────┤          │
 │       │  2. Call service layer                                           │          │
 │       │     result = await self.login_service.run(request)               │          │
 │       ├──────────────────────────────────────────────────────────────────┤          │
 │       │  3. Format response                                              │          │
 │       │     return BaseResponseDTO(status="SUCCESS", data=result)        │          │
 │       └──────────────────────────────────────────────────────────────────┘          │
 │                                                                                      │
 └─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                           🔧 SERVICE: UserLoginService                               │
 ├─────────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                      │
 │   async def run(self, request_dto: UserLoginRequestDTO):                            │
 │       ┌──────────────────────────────────────────────────────────────────┐          │
 │       │  1. Find user by email                                           │          │
 │       │     user = self.user_repo.retrieve_record_by_filter(             │          │
 │       │         {"email": request_dto.email}                             │          │
 │       │     )                                                            │          │
 │       │     if not user: raise NotFoundError("User not found")           │          │
 │       ├──────────────────────────────────────────────────────────────────┤          │
 │       │  2. Verify password                                              │          │
 │       │     if not bcrypt.verify(request_dto.password, user.password):   │          │
 │       │         raise AuthenticationError("Invalid credentials")         │          │
 │       ├──────────────────────────────────────────────────────────────────┤          │
 │       │  3. Generate JWT token                                           │          │
 │       │     token = self.jwt_utility.create_token(                       │          │
 │       │         user_id=user.id, user_urn=user.urn                       │          │
 │       │     )                                                            │          │
 │       ├──────────────────────────────────────────────────────────────────┤          │
 │       │  4. Update login status                                          │          │
 │       │     self.user_repo.update_record_by_filter(                      │          │
 │       │         {"id": user.id}, {"is_logged_in": True}                  │          │
 │       │     )                                                            │          │
 │       ├──────────────────────────────────────────────────────────────────┤          │
 │       │  5. Return result                                                │          │
 │       │     return {"user": user.to_dict(), "token": token}              │          │
 │       └──────────────────────────────────────────────────────────────────┘          │
 │                                                                                      │
 └─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                          🗄️ REPOSITORY: UserRepository                               │
 ├─────────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                      │
 │   def retrieve_record_by_filter(self, filters, use_or=False):                       │
 │       ┌──────────────────────────────────────────────────────────────────┐          │
 │       │  1. Build SQLAlchemy query                                       │          │
 │       │     query = self.session.query(User)                             │          │
 │       │                                                                  │          │
 │       │  2. Apply filters with operators                                 │          │
 │       │     Supports: EQ, NE, GT, LT, GTE, LTE, LIKE, IN, IS_NULL       │          │
 │       │     query = query.filter(User.email == "user@example.com")       │          │
 │       │                                                                  │          │
 │       │  3. Execute and return                                           │          │
 │       │     return query.first()                                         │          │
 │       └──────────────────────────────────────────────────────────────────┘          │
 │                                          │                                          │
 │                                          ▼                                          │
 │                              ┌───────────────────────┐                              │
 │                              │   🐘 PostgreSQL       │                              │
 │                              │   SELECT * FROM users │                              │
 │                              │   WHERE email = ?     │                              │
 │                              └───────────────────────┘                              │
 │                                                                                      │
 └─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                              📤 OUTGOING RESPONSE                                    │
 ├─────────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                      │
 │   HTTP/1.1 200 OK                                                                   │
 │   Content-Type: application/json                                                    │
 │   X-Request-ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV                                         │
 │   X-Process-Time: 0.045s                                                            │
 │   X-RateLimit-Remaining: 59                                                         │
 │   Strict-Transport-Security: max-age=31536000; includeSubDomains                   │
 │   Content-Security-Policy: default-src 'self'                                       │
 │                                                                                      │
 │   {                                                                                  │
 │       "transactionUrn": "01ARZ3NDEKTSV4RRFFQ69G5FAV",                              │
 │       "status": "SUCCESS",                                                          │
 │       "responseMessage": "User logged in successfully",                             │
 │       "responseKey": "success_user_login",                                          │
 │       "data": {                                                                      │
 │           "user": { "id": 1, "email": "user@example.com" },                         │
 │           "token": "eyJhbGciOiJIUzI1NiIs..."                                        │
 │       }                                                                              │
 │   }                                                                                  │
 │                                                                                      │
 └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔀 MVC Layer Interactions

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│    📨 DTOs                    🎮 CONTROLLER                   🔧 SERVICE            │
│   (Validation)               (HTTP Handler)               (Business Logic)          │
│                                                                                      │
│  ┌─────────────┐            ┌─────────────┐              ┌─────────────┐            │
│  │ RequestDTO  │───────────▶│  validate   │─────────────▶│    run()    │            │
│  │             │  Pydantic  │  & parse    │   Inject     │             │            │
│  │ • email     │  validates │             │   service    │ • business  │            │
│  │ • password  │            │  post()     │              │   rules     │            │
│  │ • metadata  │            │  get()      │              │ • workflows │            │
│  └─────────────┘            │  put()      │              │ • validation│            │
│                             │  delete()   │              │             │            │
│  ┌─────────────┐            └──────┬──────┘              └──────┬──────┘            │
│  │ ResponseDTO │◀──────────────────┘                            │                   │
│  │             │    Format                                      │                   │
│  │ • status    │    response                                    ▼                   │
│  │ • message   │                                         ┌─────────────┐            │
│  │ • data      │                                         │ REPOSITORY  │            │
│  └─────────────┘                                         │             │            │
│                                                          │ • CRUD ops  │            │
│                                                          │ • filtering │            │
│                                                          │ • caching   │            │
│                                                          └──────┬──────┘            │
│                                                                 │                   │
│                                                                 ▼                   │
│                                                          ┌─────────────┐            │
│                                                          │   MODEL     │            │
│                                                          │             │            │
│                                                          │ • ORM entity│            │
│                                                          │ • relations │            │
│                                                          │ • methods   │            │
│                                                          └─────────────┘            │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
my_api/
├── 🎯 app.py                 # FastAPI entry point
├── ⚙️ start_utils.py         # Startup configuration
│
├── 📋 abstractions/          # Base classes & interfaces
│   ├── controller.py         # IController
│   ├── service.py            # IService
│   └── repository.py         # IRepository with filters
│
├── 🎮 controllers/           # HTTP route handlers
│   └── user/
│       ├── login.py
│       ├── logout.py
│       └── register.py
│
├── 🔧 services/              # Business logic layer
│   └── user/
│       ├── login.py
│       └── registration.py
│
├── 🗄️ repositories/          # Data access layer
│   └── user.py
│
├── 📊 models/                # SQLAlchemy ORM models
│   └── user.py
│
├── 📨 dtos/                  # Data Transfer Objects
│   ├── requests/             # Input validation
│   └── responses/            # Output formatting
│
├── 🛡️ middlewares/           # Request processing
│   ├── authentication.py     # JWT validation
│   ├── rate_limit.py         # Rate limiting
│   └── security_headers.py   # Security headers
│
├── 🔄 migrations/            # Alembic migrations
│   └── versions/
│
├── 🧪 tests/                 # Test suite
│   └── unit/
│
└── 🐳 docker-compose.yml     # PostgreSQL + Redis
```

---

## 📋 API Response Format

All responses follow a consistent structure:

```json
{
    "transactionUrn": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "status": "SUCCESS",
    "responseMessage": "User logged in successfully",
    "responseKey": "success_user_login",
    "data": {
        "user": {
            "id": 1,
            "email": "user@example.com"
        },
        "token": "eyJhbGciOiJIUzI1NiIs..."
    }
}
```

| Field | Description |
|-------|-------------|
| `transactionUrn` | Unique request identifier for tracing |
| `status` | `SUCCESS` or `FAILED` |
| `responseMessage` | Human-readable message |
| `responseKey` | Machine-readable key for i18n |
| `data` | Response payload |

---

## 🛡️ Middleware Stack

FastMVC uses [**fastmvc-middleware**](https://pypi.org/project/fastmvc-middleware/) - a collection of **90+ production-ready middlewares** for FastAPI:

```python
from fastmiddleware import (
    SecurityHeadersMiddleware,    # CSP, HSTS, X-Frame-Options
    RateLimitMiddleware,          # Sliding window rate limiting
    RequestContextMiddleware,     # Request tracking & URN generation
    TimingMiddleware,             # Response time headers
    LoggingMiddleware,            # Structured request logging
    CORSMiddleware,               # Cross-origin resource sharing
    # ... and 80+ more!
)
```

### Available Middleware Categories

| Category | Examples |
|----------|----------|
| **Security** | SecurityHeaders, CSRF, HTTPS Redirect, IP Filter, Honeypot |
| **Rate Limiting** | RateLimit, Quota, Load Shedding, Bulkhead |
| **Authentication** | JWT Auth, API Key, Basic Auth, Bearer Auth |
| **Caching** | Response Cache, ETag, Conditional Request |
| **Observability** | Logging, Timing, Metrics, Correlation ID |
| **Resilience** | Circuit Breaker, Timeout, Retry, Graceful Shutdown |

---

## 🔐 Security Features

| Feature | Description |
|---------|-------------|
| 🔑 **JWT Authentication** | Secure token-based auth with configurable expiry |
| 🔒 **Password Hashing** | Bcrypt with configurable salt rounds |
| 🚦 **Rate Limiting** | Sliding window algorithm (per-minute & per-hour) |
| 🛡️ **Security Headers** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options |
| 🔍 **Input Validation** | SQL injection, XSS, and path traversal detection |
| 📍 **Request Tracing** | Unique URN for every request (debugging & monitoring) |

---

## ⚙️ Configuration

### Environment Variables

```bash
# .env file
# JWT
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastmvc
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
BCRYPT_SALT=$2b$12$...
```

---

## 🐳 Docker

```bash
# Start all services (PostgreSQL + Redis)
docker-compose up -d

# View logs
docker-compose logs -f fastapi

# Stop everything
docker-compose down

# Reset (including volumes)
docker-compose down -v
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/services/test_user_services.py -v

# Run with verbose output
pytest -v --tb=short
```

---

## 📖 Documentation

| Module | Description |
|--------|-------------|
| [📋 Abstractions](abstractions/README.md) | Base interfaces & contracts |
| [⚙️ Configurations](configurations/README.md) | Config loaders |
| [📊 Constants](constants/README.md) | Application constants |
| [🎮 Controllers](controllers/README.md) | Route handlers |
| [💉 Dependencies](dependencies/README.md) | DI factories |
| [📨 DTOs](dtos/README.md) | Data transfer objects |
| [❌ Errors](errors/README.md) | Custom exceptions |
| [🛡️ Middlewares](middlewares/README.md) | Request middleware |
| [🔄 Migrations](migrations/README.md) | Database migrations |
| [🗄️ Models](models/README.md) | SQLAlchemy models |
| [📦 Repositories](repositories/README.md) | Data access |
| [🔧 Services](services/README.md) | Business logic |
| [🔨 Utilities](utilities/README.md) | Helper functions |
| [⚡ CLI](fastmvc_cli/README.md) | Command line interface |

---

## 🤝 Contributing

We love contributions! Here's how to get started:

```bash
# Clone the repo
git clone https://github.com/shregar1/fastMVC.git
cd fastMVC

# Using uv (recommended)
uv sync --all-extras
uv run pytest

# Or using pip
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
pytest

# Make your changes and submit a PR!
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

### Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/)

**⭐ Star us on GitHub if this helped you!**

[Report Bug](https://github.com/shregar1/fastMVC/issues) •
[Request Feature](https://github.com/shregar1/fastMVC/issues) •
[Discussions](https://github.com/shregar1/fastMVC/discussions)

</div>
