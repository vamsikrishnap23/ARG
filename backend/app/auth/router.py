from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models import UserCreate, UserLogin, Token, UserDB, UserRole
from app.auth.utils import get_password_hash, verify_password, create_access_token, get_current_user
from app.db import get_supabase
from app.config import settings
from supabase import Client

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, supabase: Client = Depends(get_supabase)):
    # Check if user already exists
    user_data = supabase.table("users").select("*").eq("email", user.email).execute()
    if user_data.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user in Supabase Auth
    try:
        auth_user = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        user_id = auth_user.user.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )
    
    # Store additional user data in users table
    hashed_password = get_password_hash(user.password)
    new_user = {
        "id": user_id,
        "email": user.email,
        "username": user.username,
        "password_hash": hashed_password,
        "role": UserRole.PLAYER
    }
    
    supabase.table("users").insert(new_user).execute()
    
    # Create initial profile
    profile_data = {
        "user_id": user_id,
        "username": user.username,
        "current_level": 1,
        "total_score": 0,
        "last_login": "now()"
    }
    supabase.table("profiles").insert(profile_data).execute()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id, "role": UserRole.PLAYER},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), supabase: Client = Depends(get_supabase)):
    # Authenticate with Supabase
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": form_data.username,  # OAuth2 form uses username field for email
            "password": form_data.password
        })
        user_id = auth_response.user.id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user data from our users table
    user_data = supabase.table("users").select("*").eq("id", user_id).execute()
    if not user_data.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_data.data[0]
    
    # Update last login
    supabase.table("profiles").update({"last_login": "now()"}).eq("user_id", user_id).execute()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id, "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

