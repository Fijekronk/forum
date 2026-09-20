from pydantic import BaseModel
from datetime import datetime

class UserReg(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime 

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    token: str