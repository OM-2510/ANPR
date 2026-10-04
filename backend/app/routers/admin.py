from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin import AdminLogin, Token
from app.crud.admin import get_admin_by_username
from app.core.security import verify_password, create_access_token
from app.deps import get_current_admin

router = APIRouter()

@router.post("/admin/login")
def admin_login(credentials: AdminLogin,  db: Session=Depends(get_db)):
    admin = get_admin_by_username(db, credentials.username)
    if admin is None or not verify_password(credentials.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Username or Password!")
    token = create_access_token({"sub": admin.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/admin/me")
def admin_me(admin=Depends(get_current_admin)):
    return {"username": admin.username}
