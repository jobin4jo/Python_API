# schemas.py

from pydantic import BaseModel
from pydantic import BaseModel, Field
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class UserRegistration (BaseModel):
    name: str=Field(...,min_length=3, max_length=20) 
    email: str=Field(...,min_length=3, max_length=20) 
    password: str=Field(...,min_length=3, max_length=20) 

class Token(BaseModel):
    access_token: str
    token_type: str

class loginrequest(BaseModel):
    name: str=Field(...,min_length=3, max_length=20)    
    password: str=Field(...,min_length=5)