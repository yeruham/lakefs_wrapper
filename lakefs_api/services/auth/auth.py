from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status

from ...core.database import _users_collection
from ...core.config import get_settings
from ...core.security import create_access_token, verify_password
from ...models import AuthCapabilities, AuthenticationToken, LoginInformation


async def get_auth_capabilities() -> AuthCapabilities:
    return AuthCapabilities(invite_user=True, forgot_password=False)


async def login(body: Optional[LoginInformation]) -> AuthenticationToken:
    if body is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing body")

    doc = await _users_collection().find_one(
        {"credentials.access_key_id": body.access_key_id},
        {"_id": 0},
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    credentials = doc.get("credentials", [])
    cred = next((c for c in credentials if c.get("access_key_id") == body.access_key_id), None)
    if cred is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(body.secret_access_key, cred.get("secret_access_key_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    expires_delta = timedelta(minutes=get_settings().access_token_expire_minutes)
    expires_at = int((datetime.now(timezone.utc) + expires_delta).timestamp())
    token = create_access_token(
        {"sub": doc["id"], "groups": doc.get("groups", [])},
        expires_delta=expires_delta,
    )
    return AuthenticationToken(token=token, token_expiration=expires_at)