from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.parking import ExitResponse
from app.crud.parking import close_parking_session

router = APIRouter()

@router.post("/exit", response_model=ExitResponse)
def exit(plate_number: str, db: Session = Depends(get_db)):
    session = close_parking_session(db, plate_number)
    if session is None:
        raise HTTPException(status_code=404, detail="Vehicle's plates are absent from database")
    else:
        return session

