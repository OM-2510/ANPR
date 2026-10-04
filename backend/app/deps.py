from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.crud.admin import get_admin_by_username

bearer = HTTPBearer()

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    admin = get_admin_by_username(db, username)

    if admin is None:
        raise HTTPException(status_code=401, detail="Admin not found")

    return admin