# Backend Architecture & Flow of Control

```text
backend/
└── app/
    ├── crud/
    ├── models/
    ├── routers/
    ├── schemas/
    └── main.py
└── parking.db

```

### 1. CRUD (Create, Read, Update, Delete)

Contains functions for all database operations required in the application.

* Uses `from sqlalchemy.orm import Session` as the connection handle to query, add, and commit data.
* Sessions are created by `SessionLocal()` and auto-opened/closed per request via `Depends(get_db)`.
* Example: `new_session = ParkingSession(plate_number=plate_number)` creates an in-memory object only. It is not in the database yet.
* Operations become real via: **`db.add()` → `db.commit()` → `db.refresh()**`.
* This relies on configurations set in `database.py`.

### 2. Models

Contains definitions, structures, and schemas for all the Relational Models (Tables) created in the database, separated into distinct files.

* Defines table names and columns using SQLAlchemy types (`Enum`, `String`, `Integer`, etc.), held together by `Column`.
* Must inherit from `Base` (configured in `database.py`). This registers the class into `Base.metadata` so `Base.metadata.create_all()` can physically create the table. Without it, the class is inert.

### 3. Routers

Routes for the API are defined here using FastAPI's **`APIRouter`** module across separate files.

* Response and Request models are imported from the **Schemas** directory.
* These individual routers are then imported into **`main.py`** to serve the routing and other core functions.

### 4. Schemas

Uses the **Pydantic** module to set up data validation for both incoming requests and outgoing responses.

* Ensures the API receives and returns exactly the expected data types.
* Has no direct interaction with the actual database.

---

## Flow of Control

1. Client hits a router (e.g., `POST /exit`).
2. Router pulls request data and gets a database session via `Depends(get_db)`.
3. Router calls a CRUD function, passing the session (`db`) and the data.
4. CRUD uses the `db` (Session) to query, insert, or update. **This is where Models (table definitions) and the actual database file get used together in the same step.**
5. CRUD returns a model object (e.g., `ParkingSession`) back to the router.
6. Router returns that object.
7. FastAPI applies the `response_model` (Schema), shaping it into JSON.
8. JSON is sent to the client.

> **Visual Flow:**
> Router → CRUD → (Models + Database, together) → CRUD → Router → Schema → JSON

---

## Configuring Security and Admin Routes

### Token Authentication Mechanisms

* **JSON Web Tokens (JWT):** A stateless token format consisting of a Header, Payload (user data/expiration), and Signature. The server validates the token purely through cryptography using a `SECRET_KEY`—no database lookup required. Highly scalable.
* **Dual-Token Architecture (OAuth 2.0):** Uses a short-lived **Access Token** (e.g., 60 mins) for daily API requests, and a long-lived **Refresh Token**. When the Access Token expires, the client silently sends the Refresh Token to a `/refresh` endpoint to get a new Access Token without logging the user out.
* **Bearer Tokens:** The standard transmission model used in this app (`Authorization: Bearer <token>`). Whoever "bears" (holds) the token gets access.
* **Server-Side (Opaque/Session) Tokens:** Random strings containing no readable data. The server must query a stateful database or cache (like Redis) on every request to verify who the token belongs to and if it is valid.
* **Legacy Tokens (Basic Auth):** An older method where the raw username and password are simply Base64-encoded and transmitted in the header of every single request. Rarely used in modern APIs due to security risks.

---

## Implementation Steps

### 1. `security.py`

* Define `hash_password` and `verify_password` functions.
* Define `create_access_token` function for JWT minting.
* **Note:** The current implementation lacks refresh tokens.
* **Dependency Note:** `bcrypt==5.0.0` and `passlib==1.7.4` clash. Downgrade to `bcrypt==4.0.1` for cryptography to function properly.

### 2. `schemas/admin.py`

* **AdminLogin:** Requires `username` and `password`.
* **Token:** Returns `access_token` and `token_type`.

### 3. CRUD and Routers

* Defined as usual, but **do not reference plain-text passwords directly anywhere**.
* Always use the `hash_password` and `verify_password` functions when creating or verifying users.

### 4. `deps.py` (Dependencies)

This file isolates reusable dependency functions so they can be easily injected into any router. It acts as the "bouncer" for the API.

* **`get_db` (Database Lifecycle):** A generator function utilizing Python's `yield`. When injected, it opens a fresh database session for the incoming HTTP request. Once the route finishes executing (or crashes), the code after the `yield` runs, guaranteeing the session is safely closed and connection limits aren't exhausted.
* **`get_current_admin` (Security Check):**
1. **Extract:** Uses `HTTPBearer()` to automatically intercept requests and extract the raw token from the `Authorization` header.
2. **Verify mathematically:** Calls `jwt.decode()` with the `SECRET_KEY`. If the signature is forged or the expiration time (`exp`) has passed, it throws a `JWTError` and immediately returns a `401 Unauthorized`.
3. **Verify statefully:** Extracts the username (`sub`) from the decoded payload and queries the database via `get_admin_by_username()`. This ensures the account wasn't deleted or suspended since the token was minted.
4. **Inject:** Returns the verified database `admin` object directly into the route.



> **Note on FastAPI `Depends`:**
> `Depends()` is FastAPI's mechanism for **Dependency Injection**. It acts as a strict prerequisite. When you define a route like `@router.get("/admin/me") def admin_me(admin = Depends(get_current_admin)):`, you are telling FastAPI: *"Do not run this route until `get_current_admin` executes successfully. If it succeeds, take whatever it returns and hand it to me as the `admin` variable."* This keeps route code completely clean of security and database-handling logic.