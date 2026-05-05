from __future__ import annotations

from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel
from ...models.auth import User, Group


class CredentialInDB(BaseModel):
    access_key_id: str
    secret_access_key_hash: str
    creation_date: int


class UserInDB(User):
    groups: list[str] = []
    credentials: list[CredentialInDB] = []
    policy_ids: list[str] = []


class GroupInDB(Group):
    members: list[str] = []
    policy_ids: list[str] = []
    acl: Optional[Any] = None


class LakeFSAction(str, Enum):
    read = "read"
    write = "write"
    delete = "delete"