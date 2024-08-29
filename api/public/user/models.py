from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from api.public.usercommunitylink.models import UserCommunityLink  # Importa la clase correctamente

class UserBase(SQLModel):
    username: str = Field(..., max_length=50, index=True, unique=True)
    email: str = Field(..., max_length=100, regex=r'^\S+@\S+\.\S+$', unique=True)
    full_name: Optional[str] = Field(None, max_length=100)
    role: str = Field(default="user", max_length=20)
    is_active: bool = Field(default=True)
    birthdate: Optional[datetime] = None
    image_url: Optional[str] = None

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    communities: list["Community"] = Relationship(back_populates="users", link_model=UserCommunityLink)
    comments: list["Comment"] = Relationship(back_populates="creator")
    debates: list["Debate"] = Relationship(back_populates="creator")

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(UserBase):
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)