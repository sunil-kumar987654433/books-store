from pydantic import BaseModel, EmailStr
import uuid
from typing import List
from datetime import datetime
from src.books.schema import Book

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    password: str
    confirm_password: str

class UserModel(BaseModel):
    uid: uuid.UUID
    email: EmailStr
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password_hash: str
    created_at: datetime
    updated_at: datetime
    books: List[Book] | None = None



class UserLogin(BaseModel):
    email: EmailStr
    password: str