from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import base64
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


class BasicUser(BaseModel):
    username: str
    groups: list[str]


# ── Password helpers ──────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ── JWT helpers ───────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_jwt(token: str = Depends(oauth2_scheme)) -> BasicUser:
    """FastAPI dependency – injects the decoded token payload."""
    payload = decode_token(token)
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return BasicUser(username=username, groups=payload.get("groups", []))


def get_current_user_basic(encoded: str) -> BasicUser:
    decoded = base64.b64decode(encoded).decode()
    access_key, secret_key = decoded.split(":")
    return BasicUser(username=access_key, groups = [])


def get_current_user(request: Request) -> BasicUser:
    auth = request.headers.get("Authorization")

    if not auth:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    if auth.startswith("Bearer "):
        token = auth.replace("Bearer ", "")
        return get_current_user_jwt(token=token)

    if auth.startswith("Basic "):
        encoded = auth.replace("Basic ", "")
        return get_current_user_basic(encoded=encoded)

    raise HTTPException(status_code=401, detail="Unsupported auth type")
