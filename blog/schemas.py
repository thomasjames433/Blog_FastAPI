from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config:
        from_attributes = True  # ✅ Use this in Pydantic v2


class AppUser(BaseModel):
    name:str
    email:str
    password:str

class ShowAppUser(BaseModel):
    name:str
    email:str
    blogs:List[Blog]=[]

    class Config:
        from_attributes = True

class ShowBlog(BaseModel):
    title:str
    created_by:ShowAppUser
    class Config:
        from_attributes = True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
