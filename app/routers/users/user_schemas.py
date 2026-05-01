from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserPayload(BaseModel):
    user_id: str
    full_name: str
    username: str
    email: str
    phone_number: str | None = None
    is_active: bool
    is_superuser: bool
    role: str
    login_type: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    status: str
    message: str
    payload: Optional[UserPayload | dict | list] = None