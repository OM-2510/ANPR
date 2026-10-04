from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.core.security import hash_password

def create_admin_account(db: Session, username: str, password: str):
    new_admin = Admin(
        username=username,
        hashed_password=hash_password(password)
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin

def get_admin_by_username(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()