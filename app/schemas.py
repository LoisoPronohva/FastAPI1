from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserInDB(UserBase):
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPublic(UserInDB):
    pass


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None


# Login Schemas
class LoginRequest(BaseModel):
    username: str
    password: str


# Advertisement Schemas (существующие + обновление)
class AdvertisementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    author: str = Field(..., min_length=1, max_length=100)


class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    author: Optional[str] = Field(None, min_length=1, max_length=100)


class Advertisement(AdvertisementBase):
    id: int
    owner_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)