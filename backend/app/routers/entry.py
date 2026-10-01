from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.parking import create_parking_session
from app.schemas.parking import EntryResponse

router = APIRouter()

@router.post("/upload_plates", response_model=EntryResponse)
def upload_plates(plate_number: str, db: Session = Depends(get_db)):
    session = create_parking_session(db, plate_number)
    return session

