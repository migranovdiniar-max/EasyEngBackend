from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from utils.jwt import verify_verification_token
from utils.mail import send_verification_email
from database import get_db
from models import User
from schemas.user import UserCreate, UserResponse
from utils.auth import (
    hash_password, 
    create_access_token,
    verify_password
)


router = APIRouter(
    prefix="/auth", tags=["auth"]
)

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    hashed = hash_password(user.password)

    db_user = User(
        email=user.email,
        hashed_password=hashed,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token(data={"sub": user.email})  # ← словарь
    
    await send_verification_email(user.email, token)

    return db_user


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(
        data={
            "sub": db_user.email, "id": db_user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "created_at": db_user.created_at
        }
    }


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_verification_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        return {
            "message": "Email already verified"
        }
    
    user.is_verified = True
    db.commit()