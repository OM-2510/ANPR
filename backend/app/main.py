from fastapi import FastAPI
from app.database import engine, Base
from app.routers.entry import router as entry_router
from app.routers.exit import router as exit_router
from app.routers.admin import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(entry_router)
app.include_router(exit_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"status": "ANPR backend running"}