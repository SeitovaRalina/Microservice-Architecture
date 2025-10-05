from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from src.db import get_db
from src.schemas import UserCreate, UserLogin, UserOut, TokenResponse, UserUpdate
from src.controllers import auth as auth_ctrl
from src.controllers.auth import create_access_token

router = APIRouter()

@router.post("/users", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = auth_ctrl.create_user(db, user_in)
    return user

@router.post("/users/login", response_model=TokenResponse)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    email = form_data.get("email")
    password = form_data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    user = auth_ctrl.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": user.id}, expires_delta=timedelta(minutes=int(60)))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user", response_model=UserOut)
def get_current_user(user=Depends(auth_ctrl.get_current_user)):
    return user

@router.put("/user", response_model=UserOut)
def update_user(payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(auth_ctrl.get_current_user)):
    if payload.email:
        current_user.email = payload.email
    if payload.username:
        current_user.username = payload.username
    if payload.password:
        current_user.password_hash = auth_ctrl.get_password_hash(payload.password)
    if payload.bio is not None:
        current_user.bio = payload.bio
    if payload.image_url is not None:
        current_user.image_url = payload.image_url
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
