from app.routers.auth.auth_schemas import AuthResponse, UserCreate, UserLogin
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.routers.auth.auth_model import User
from app.routers.auth.auth_validators import Validators
from app.routers.auth.auth_utils import Utils
from datetime import datetime, timezone, timedelta

EAT = timezone(timedelta(hours=3))

class AuthController:
    def __init__(self):
        pass
        
    async def register(self, user_create: UserCreate, db: Session) -> AuthResponse:
        try:
            existing_user = await db.execute(select(User).where(User.username == user_create.username))
            existing_email = await db.execute(select(User).where(User.email == user_create.email))
            
            print("Existing user query result:", existing_user)
            print("Existing email query result:", existing_email)
            
            if existing_user.scalar() or existing_email.scalar():
                raise HTTPException(status_code=400, detail="Username or email already registered")
            
            if not Validators.validate_email(user_create.email):
                raise HTTPException(status_code=400, detail="Invalid email format")
            
            if not Validators.validate_password(user_create.password):
                raise HTTPException(status_code=400, detail="Password does not meet strength requirements")
            
            new_user = User(
                full_name=user_create.full_name,
                username=user_create.username,
                email=user_create.email,
                phone_number=user_create.phone_number,
                created_at=datetime.now(EAT).isoformat(),
                updated_at=datetime.now(EAT).isoformat()
            )
            
            new_user.set_password(user_create.password)
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            return AuthResponse(
                status="success",
                message="Success", 
                payload="User registered successfully"
            )
        
        except HTTPException as e:
            return AuthResponse(status="error", message=e.detail)
        except Exception as e:
            return AuthResponse(status="error", message=str(e))

    async def login(self, user_login: UserLogin, db: Session) -> AuthResponse:
        try:
            existing_user = await db.execute(select(User).where(User.username == user_login.username))
            existing_user = existing_user.scalar_one_or_none()
            
            if not existing_user:
                raise HTTPException(status_code=400, detail="User not found")
            
            validate_password = existing_user.check_password(user_login.password)
            
            if not validate_password:
                raise HTTPException(status_code=400, detail="Incorrect password")
            
            token = existing_user.jwt_sign_user_payload()
            
            return AuthResponse(
                status="success",
                message="Login successful",
                payload=token
            )
            
        except HTTPException as e:
            return AuthResponse(status="error", message=e.detail)
        except Exception as e:
            return AuthResponse(status="error", message=str(e))

    async def logout(self, token: str) -> AuthResponse:
        try:
            await Utils().invalidate_token(token)
            return AuthResponse(status="success", message="Logout successful")
        except Exception as e:
            return AuthResponse(status="error", message=str(e))