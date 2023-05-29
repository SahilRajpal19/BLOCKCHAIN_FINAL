from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email_id: Optional[str] = None


class Register_user(BaseModel):
    username: str
    email_id: str
    password: str


class Transaction(BaseModel):
    recipient: str
    amount: float


class UserInDB(User):
    hashed_password: str
