import jwt
from fastapi import HTTPException, status
from app.config.core.settings import settings
from functools import wraps

def validate_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def extract_token(authorization: str) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorization header must start with 'Bearer '"
        )
    return authorization[7:]

# --- Decorators ---

def requires_auth(func):
    """Validates JWT and injects payload into the method."""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        authorization = kwargs.get("authorization")
        token = extract_token(authorization)
        payload = validate_jwt(token)
        kwargs["token_payload"] = payload
        return await func(self, *args, **kwargs)
    return wrapper

def requires_admin(func):
    """Validates JWT and ensures user has admin role."""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        authorization = kwargs.get("authorization")
        token = extract_token(authorization)
        payload = validate_jwt(token)

        if payload.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this route"
            )

        kwargs["token_payload"] = payload
        return await func(self, *args, **kwargs)
    return wrapper