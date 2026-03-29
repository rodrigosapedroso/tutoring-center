from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import Token, LoginRequest, UserRead
from ..auth import authenticate_user, create_access_token, get_current_user
from ..database import get_db
from ..models import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/auth")

@router.post("/token", response_model=Token)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token_data = {"user_id": user.id, "role": user.role.value}
    access_token = create_access_token(token_data)

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role.value
    }
