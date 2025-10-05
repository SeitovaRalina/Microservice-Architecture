from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=150, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=6)
    bio: Optional[str] = None
    image_url: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ProfileOut(BaseModel):
    username: str
    bio: Optional[str]
    image_url: Optional[str]

    # @classmethod
    # def from_user(cls, user):
    #     if getattr(user, "is_deleted", False):
    #         return cls(
    #             username="Удалённый пользователь",
    #             bio=None,
    #             image_url=None
    #         )
    #     return cls.model_validate(user, from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = []

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tagList: Optional[List[str]] = None

class ArticleOut(BaseModel):
    id: int
    title: str
    description: str
    body: str
    slug: str
    tagList: List[str] = []
    author: UserOut

    model_config = ConfigDict(from_attributes=True)

class CommentCreate(BaseModel):
    body: str

class CommentOut(BaseModel):
    id: int
    body: str
    created_at: str
    author: UserOut

    model_config = ConfigDict(from_attributes=True)