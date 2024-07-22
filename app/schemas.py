from pydantic import BaseModel
from enum import Enum
from typing import List


class RoleType(str, Enum):
    admin = "admin"
    user = "user"


class TodoBase(BaseModel):
    title: str
    description: str | None = None


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleCreate):
    id: int


class UserBase(BaseModel):
    email: str
    role_id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    role: Role
    todos: list[Todo] | None = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    user_id: int | None = None
    scopes: List[str] = []
