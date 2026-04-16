from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    password: str
    confirm_password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str