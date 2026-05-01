from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str
    email: str
    phone_number: str | None = None
    
class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    full_name: str
    username: str
    email: str
    phone_number: str | None = None
    
    class Config:
        from_attributes = True
        
class AuthResponse(BaseModel):
    status: str
    message: str
    payload: UserResponse | str | None = None
    