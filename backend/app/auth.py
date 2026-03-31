import os

from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import User, UserRole
from .utils.hashing import verify_password

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
    return user

def require_teacher(user: User = Depends(get_current_user)):
    if user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Access denied")
    return user

def require_parent(user: User = Depends(get_current_user)):
    if user.role != UserRole.PARENT:
        raise HTTPException(status_code=403, detail="Access denied")
    return user