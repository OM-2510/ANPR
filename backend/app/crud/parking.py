import datetime
import math
from sqlalchemy.orm import Session
from app.models.parking_session import ParkingSession, ParkingStatus
from app.models.payment import Payment, PaymentMethod

billing_rate = 20

def create_parking_session(db: Session, plate_number: str):
    new_session = ParkingSession(plate_number = plate_number)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

def close_parking_session(db: Session, plate_number: str):
    session = db.query(ParkingSession).filter(
        ParkingSession.plate_number == plate_number,
        ParkingSession.status == ParkingStatus.PARKED
    ).first()

    if(session is None):    
        return None

    session.exit_time = datetime.datetime.utcnow()
    
    duration = session.exit_time - session.entry_time
    hours = math.ceil(duration.total_seconds() / 3600)
    session.amount = hours * billing_rate

    session.status = ParkingStatus.EXITED
    db.commit()
    db.refresh(session)
    
    return session

def create_invoice(db:Session, session_id: int, method: PaymentMethod):
    parking_rec = db.query(ParkingSession).filter(ParkingSession.id == session_id).first()

    if(parking_rec is None):
         return None

    new_invoice = Payment(
         session_id = session_id,
         amount = parking_rec.amount,
         method = method
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return new_invoice

       