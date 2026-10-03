# Progression

```
backend/
└── app/
    ├── crud/
    ├── models/
    ├── routers/
    ├── schemas/
    └── main.py
└───parking.db
```

**1. Crud:** Contains function for all database crud operations required in applicatin.

**2. Models:** Contains definiton or structure/schema for all the Relational Models or Tables that are created in our Database in seprate files. 

**3. Routers:** All the routes are defined here with help of the **APIRouter** module in seprate files. 

**4. Schemas:** Does the data validation for Response and Request body has no contribution or direct interaction with actual database itself.

# 1. CRUD

```
from sqlalchemy.orm import Session
```
SQLAlchemy's connection handle, used to query/add/commit.
Created by SessionLocal(), auto-opened+closed per request via Depends(get_db).

```
new_session = ParkingSession(plate_number = plate_number)
```
creates an in-memory object only. Not in DB yet. id/entry_time still empty
those operations are done later, i.e.

**→ db.add() → db.commit() → db.refresh() make it real.**

**for this to function we configure database.py**

# 2. MODELS

Define tablenames + columns using SQLAlchemy types (Enum, String, Integer etc.), held together by Column.

Must inherit from Base (database.py) — this is what registers the class into Base.metadata so create_all() can actually create the table. Without it, the class is inert.

# 3. ROUTERS

we define the routes for our website using various file with **APIRouter**. We'd import our **ResponseModels** and **RequestModels** from **Schema** file. Then again these routes are imported to **main.py** to serve the routing and other funtions.

# 4. SCHEMAS

using the **pydantic** module we setup the data validation for routes for both request and response routes and for the **API** to work properly.

# Flow of Control

1. Client hits a router (e.g. POST /exit)
2. Router pulls request data + gets db session via Depends(get_db)
3. Router calls a crud function, passing db + data
4. Crud uses db (Session) to query/insert/update — this is where
   Models (table defs) + the actual database file get used, together,
   not as separate steps
5. Crud returns a model object (e.g. ParkingSession) back to router
6. Router returns that object
7. FastAPI applies response_model (Schema) → shapes it into JSON
8. JSON → client

Key: Schema only touches data on the way OUT (or validating what
comes IN) — never during the DB operation itself.

**Diagram**

<hr>

**router → crud → (models + database, together, same step) → back to crud → back to router → schema → JSON**
