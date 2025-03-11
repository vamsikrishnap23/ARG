from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "admin"
    PLAYER = "player"

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDB(UserBase):
    id: str
    role: UserRole = UserRole.PLAYER
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str
    role: UserRole

class ProfileBase(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class ProfileUpdate(ProfileBase):
    pass

class LevelProgress(BaseModel):
    level_id: int
    completed: bool = False
    score: int = 0
    completed_at: Optional[datetime] = None

class ProfileDB(ProfileBase):
    user_id: str
    progress: List[LevelProgress] = []
    current_level: int = 1
    total_score: int = 0
    last_login: datetime

