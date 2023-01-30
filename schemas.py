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