from sqlalchemy.orm import Session
from app.models.parking_session import ParkingSession

def create_parking_session(db: Session, plate_number: str):
    new_session = ParkingSession(plate_number = plate_number)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session
