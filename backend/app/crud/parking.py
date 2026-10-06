import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.parking_session import ParkingSession, ParkingStatus
from app.models.payment import Payment, PaymentMethod
from app.services.billing import calculate_fee_and_durtation
from app.services.time import start_of_today

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
    
    amount, duration = calculate_fee_and_durtation(session.entry_time, session.exit_time)
    session.amount = amount
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

def get_parked_vehicles(db: Session):
    parked_vehicles = db.query(ParkingSession).filter(ParkingSession.status == ParkingStatus.PARKED).all()

    return parked_vehicles 

def get_history(db: Session):
    history = db.query(ParkingSession).filter(ParkingSession.status.in_([ParkingStatus.EXITED, ParkingStatus.PAID])).order_by(ParkingSession.exit_time.desc()).limit(100).all()    
    return history

def get_stats(db: Session):
    currently_parked = db.query(func.count(ParkingSession.id)).filter(ParkingSession.status==ParkingStatus.PARKED).scalar()
    entries_today = db.query(func.count(ParkingSession.id)).filter(ParkingSession.entry_time >= start_of_today()).scalar()
    exits_today = db.query(func.count(ParkingSession.id)).filter(ParkingSession.exit_time >= start_of_today()).scalar()
    revenue_today = db.query(func.coalesce(func.sum(ParkingSession.amount), 0)).filter(
        ParkingSession.exit_time >= start_of_today(),
        ParkingSession.status.in_([ParkingStatus.EXITED, ParkingStatus.PAID])
    ).scalar()

    return {
        "currently_parked": currently_parked,
        "entries_today": entries_today,
        "exits_today": exits_today,
        "revenue_today": revenue_today,
    }

