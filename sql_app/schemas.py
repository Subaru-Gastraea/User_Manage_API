from datetime import date, datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    birthday: date

class UserCreate(UserBase):
    password: str

class User(UserBase):
    createT: datetime
    last_login: datetime | None = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None