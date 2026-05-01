from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.database import get_db
from app.routers.auth.auth_schemas import AuthResponse, UserCreate, UserLogin
from app.routers.auth.auth_controller import AuthController

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

auth_controller = AuthController()
        
@router.post("/register", response_model=AuthResponse)
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        return await auth_controller.register(user_create, db)
    except Exception as e:
        return AuthResponse(status="error", message=str(e))
    
@router.post("/login", response_model=AuthResponse)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    try:
        return await auth_controller.login(user_login, db)
    except Exception as e:
        return AuthResponse(status="error", message=str(e))
    
@router.post("/logout", response_model=AuthResponse)
async def logout(token: str):
    try:
        return await auth_controller.logout(token)
    except Exception as e:
        return AuthResponse(status="error", message=str(e))
    