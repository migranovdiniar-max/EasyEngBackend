from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import os
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from utils.jwt import create_verification_token, verify_access_token, verify_verification_token
from utils.mail import send_verification_email
from database import get_db
from models import User
from schemas.user import UserCreate, UserResponse
from utils.auth import (
    hash_password, 
    create_access_token,
    verify_password
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

    print("\n" + "="*50)
    print("TOKEN FOR COPY:")
    print(token)
    print("="*50 + "\n")

    return db_user


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == request.username).first()
    
    if not db_user or not verify_password(request.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(
        data={"sub": db_user.email, "id": db_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
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


@router.post("resend-verification")
def resend_verification(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
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
    
    token = create_verification_token(user.email)
    
    background_tasks.add_task(
        send_verification_email, user.email, token
    )

    dev_mode = os.getenv("DEV_MODE", "False").lower() == "True"

    response = {
        "message": "Verification email sent",
        "token": token
    }
    if dev_mode:
        response['verification_token'] = token
        response["verify_url"] = f"http://localhost:8000/auth/verify-email?token={token}"
    
    return response


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return user