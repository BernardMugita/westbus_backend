from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as SqlEnum
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.settings import settings
from app.routers.core.models import Base
import uuid
import jwt

class UserRoles(str, Enum):
    USER = "user"
    ADMIN = "admin"
    
class LoginTypes(str, Enum):
    EMAIL_PASSWORD = "email_password"
    GOOGLE_OAUTH = "google_oauth"

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    
    role: Mapped[UserRoles] = mapped_column(SqlEnum(UserRoles), default=UserRoles.USER)
    login_type: Mapped[LoginTypes] = mapped_column(SqlEnum(LoginTypes), default=LoginTypes.EMAIL_PASSWORD)
    
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(50), nullable=False)
    
    def jwt_sign_user_payload(self):
        user_payload = {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "login_type": self.login_type.value,
        }
        
        token = jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "role": self.role.value,
            "login_type": self.login_type.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }   
        
    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)