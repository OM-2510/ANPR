from fastapi import FastAPI
from app.database import engine, Base
from app.routers.entry import router as entry_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(entry_router)

@app.get("/")
def root():
    return {"status": "ANPR backend running"}