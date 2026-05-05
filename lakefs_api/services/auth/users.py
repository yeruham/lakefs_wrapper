from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import HTTPException, status

from .schemas import UserInDB
from ...core.database import _users_collection, _groups_collection, _policies_collection
from ...core.security import hash_password
from ...models import (
    Credentials,
    CredentialsList,
    CredentialsWithSecret,
    CurrentUser,
    Group,
    GroupList,
    Pagination,
    Policy,
    PolicyList,
    User,
    UserCreation,
    UserList,
)
from .utils import _now_ts, _paginate


def _user_from_doc(doc: dict[str, Any]) -> User:
    return User(
        id=doc["id"],
        creation_date=doc.get("creation_date", 0),
        friendly_name=doc.get("friendly_name"),
        email=doc.get("email"),
    )


async def get_current_user(current_user: dict[str, Any]) -> CurrentUser:
    doc = await _users_collection().find_one({"id": current_user["username"]}, {"_id": 0})
    if doc:
        return CurrentUser(user=_user_from_doc(doc))
    return CurrentUser(user=User(id=current_user["username"], creation_date=0))


async def list_users(prefix: Optional[str], after: Optional[str], amount: Optional[int]) -> UserList:
    query: dict[str, Any] = {}
    if prefix:
        query["id"] = {"$regex": f"^{prefix}"}
    docs = await _users_collection().find(query, {"_id": 0}).sort("id", 1).to_list(length=None)
    items = [_user_from_doc(d) for d in docs]
    paged, has_more, next_offset = _paginate(items, "id", after, amount)
    return UserList(
        pagination=Pagination(
            has_more=has_more,
            next_offset=next_offset,
            results=len(paged),
            max_per_page=max(0, amount or len(paged)),
        ),
        results=paged,
    )


async def create_user(body: Optional[UserCreation]) -> User:
    if body is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing body")
    exists = await _users_collection().find_one({"id": body.id}, {"_id": 1})
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    doc = {
        "id": body.id,
        "creation_date": _now_ts(),
        "friendly_name": None,
        "email": None,
        "groups": [],
        "credentials": [],
        "policy_ids": [],
    }
    await _users_collection().insert_one(doc)
    return _user_from_doc(doc)


async def get_user(user_id: str) -> User:
    doc = await _users_collection().find_one({"id": user_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _user_from_doc(doc)


async def delete_user(user_id: str) -> None:
    res = await _users_collection().delete_one({"id": user_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await _groups_collection().update_many({}, {"$pull": {"members": user_id}})


async def list_user_credentials(
    user_id: str, prefix: Optional[str], after: Optional[str], amount: Optional[int]
) -> CredentialsList:
    doc = await _users_collection().find_one({"id": user_id}, {"_id": 0, "credentials": 1})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    creds = [
        Credentials(
            access_key_id=c["access_key_id"],
            creation_date=c["creation_date"],
        )
        for c in doc.get("credentials", [])
        if prefix is None or c["access_key_id"].startswith(prefix)
    ]
    creds.sort(key=lambda c: c.access_key_id)
    paged, has_more, next_offset = _paginate(creds, "access_key_id", after, amount)
    return CredentialsList(
        pagination=Pagination(
            has_more=has_more,
            next_offset=next_offset,
            results=len(paged),
            max_per_page=max(0, amount or len(paged)),
        ),
        results=paged,
    )


async def create_credentials(user_id: str) -> CredentialsWithSecret:
    doc = await _users_collection().find_one({"id": user_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    access_key_id = secrets.token_urlsafe(12)[:20]
    secret_access_key = secrets.token_urlsafe(32)
    cred_doc = {
        "access_key_id": access_key_id,
        "secret_access_key_hash": hash_password(secret_access_key),
        "creation_date": _now_ts(),
    }
    await _users_collection().update_one({"id": user_id}, {"$push": {"credentials": cred_doc}})
    return CredentialsWithSecret(
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        creation_date=cred_doc["creation_date"],
    )


async def delete_credentials(user_id: str, access_key_id: str) -> None:
    doc = await _users_collection().find_one({"id": user_id}, {"_id": 0, "credentials": 1})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    exists = any(c["access_key_id"] == access_key_id for c in doc.get("credentials", []))
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    await _users_collection().update_one({"id": user_id}, {"$pull": {"credentials": {"access_key_id": access_key_id}}})


async def get_credentials(user_id: str, access_key_id: str) -> Credentials:
    doc = await _users_collection().find_one({"id": user_id}, {"_id": 0, "credentials": 1})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    cred = next((c for c in doc.get("credentials", []) if c["access_key_id"] == access_key_id), None)
    if cred is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return Credentials(access_key_id=cred["access_key_id"], creation_date=cred["creation_date"])


async def list_user_groups(user_id: str, prefix: Optional[str], after: Optional[str], amount: Optional[int]) -> GroupList:
    doc = await _users_collection().find_one({"id": user_id}, {"_id": 0, "groups": 1})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    group_ids: list[str] = doc.get("groups", [])
    group_docs = await _groups_collection().find({"id": {"$in": group_ids}}, {"_id": 0}).sort("id", 1).to_list(length=None)
    groups = [
        Group(id=g["id"], name=g.get("name"), description=g.get("description"), creation_date=g.get("creation_date", 0))
        for g in group_docs
        if prefix is None or g["id"].startswith(prefix)
    ]
    paged, has_more, next_offset = _paginate(groups, "id", after, amount)
    return GroupList(
        pagination=Pagination(
            has_more=has_more,
            next_offset=next_offset,
            results=len(paged),
            max_per_page=max(0, amount or len(paged)),
        ),
        results=paged,
    )


async def list_user_policies(
    user_id: str, prefix: Optional[str], after: Optional[str], amount: Optional[int], effective: Optional[bool]
) -> PolicyList:
    user = await _users_collection().find_one({"id": user_id}, {"_id": 0, "policy_ids": 1, "groups": 1})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    policy_ids = set(user.get("policy_ids", []))
    if effective:
        group_docs = await _groups_collection().find(
            {"id": {"$in": user.get("groups", [])}},
            {"_id": 0, "policy_ids": 1},
        ).to_list(length=None)
        for g in group_docs:
            policy_ids.update(g.get("policy_ids", []))

    docs = await _policies_collection().find({"id": {"$in": list(policy_ids)}}, {"_id": 0}).sort("id", 1).to_list(length=None)
    policies = [Policy.model_validate(d) for d in docs if prefix is None or d["id"].startswith(prefix)]
    paged, has_more, next_offset = _paginate(policies, "id", after, amount)
    return PolicyList(
        pagination=Pagination(
            has_more=has_more,
            next_offset=next_offset,
            results=len(paged),
            max_per_page=max(0, amount or len(paged)),
        ),
        results=paged,
    )


async def attach_policy_to_user(user_id: str, policy_id: str) -> None:
    res = await _users_collection().update_one({"id": user_id}, {"$addToSet": {"policy_ids": policy_id}})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


async def detach_policy_from_user(user_id: str, policy_id: str) -> None:
    u = await _users_collection().find_one({"id": user_id}, {"_id": 1})
    p = await _policies_collection().find_one({"id": policy_id}, {"_id": 1})
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    await _users_collection().update_one({"id": user_id}, {"$addToSet": {"policy_ids": policy_id}})