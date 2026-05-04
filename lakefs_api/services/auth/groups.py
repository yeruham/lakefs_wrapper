from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import HTTPException, status

from ...core.database import _users_collection, _groups_collection, _policies_collection
from ...models import ACL, Group, GroupCreation, GroupList, Pagination, Policy, PolicyList, User, UserList
from .utils import _now_ts, _paginate


def _group_from_doc(doc: dict[str, Any]) -> Group:
    return Group(
        id=doc["id"],
        name=doc.get("name"),
        description=doc.get("description"),
        creation_date=doc.get("creation_date", 0),
    )


async def list_groups(prefix: Optional[str], after: Optional[str], amount: Optional[int]) -> GroupList:
    query: dict[str, Any] = {}
    if prefix:
        query["id"] = {"$regex": f"^{prefix}"}
    docs = await _groups_collection().find(query, {"_id": 0}).sort("id", 1).to_list(length=None)
    groups = [_group_from_doc(d) for d in docs]
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


async def create_group(body: Optional[GroupCreation]) -> Group:
    if body is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing body")
    exists = await _groups_collection().find_one({"id": body.id}, {"_id": 1})
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group already exists")
    doc = {
        "id": body.id,
        "name": body.id,
        "description": body.description,
        "creation_date": _now_ts(),
        "members": [],
        "policy_ids": [],
        "acl": None,
    }
    await _groups_collection().insert_one(doc)
    return _group_from_doc(doc)


async def get_group(group_id: str) -> Group:
    doc = await _groups_collection().find_one({"id": group_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return _group_from_doc(doc)


async def delete_group(group_id: str) -> None:
    res = await _groups_collection().delete_one({"id": group_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    await _users_collection().update_many({}, {"$pull": {"groups": group_id}})


async def set_group_acl(group_id: str, body: ACL) -> None:
    res = await _groups_collection().update_one({"id": group_id}, {"$set": {"acl": body.model_dump()}})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")


async def get_group_acl(group_id: str) -> ACL:
    doc = await _groups_collection().find_one({"id": group_id}, {"_id": 0, "acl": 1})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    acl_doc = doc.get("acl")
    if not acl_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ACL not set")
    return ACL.model_validate(acl_doc)


async def list_group_members(group_id: str, prefix: Optional[str], after: Optional[str], amount: Optional[int]) -> UserList:
    group = await _groups_collection().find_one({"id": group_id}, {"_id": 0, "members": 1})
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    user_docs = await _users_collection().find(
        {"id": {"$in": group.get("members", [])}},
        {"_id": 0},
    ).sort("id", 1).to_list(length=None)
    users = [
        User(
            id=d["id"],
            creation_date=d.get("creation_date", 0),
            friendly_name=d.get("friendly_name"),
            email=d.get("email"),
        )
        for d in user_docs
        if prefix is None or d["id"].startswith(prefix)
    ]
    paged, has_more, next_offset = _paginate(users, "id", after, amount)
    return UserList(
        pagination=Pagination(
            has_more=has_more,
            next_offset=next_offset,
            results=len(paged),
            max_per_page=max(0, amount or len(paged)),
        ),
        results=paged,
    )


async def add_group_membership(group_id: str, user_id: str) -> None:
    g = await _groups_collection().find_one({"id": group_id}, {"_id": 1})
    u = await _users_collection().find_one({"id": user_id}, {"_id": 1})
    if not g or not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group or user not found")
    await _groups_collection().update_one({"id": group_id}, {"$addToSet": {"members": user_id}})
    await _users_collection().update_one({"id": user_id}, {"$addToSet": {"groups": group_id}})


async def delete_group_membership(group_id: str, user_id: str) -> None:
    g = await _groups_collection().find_one({"id": group_id}, {"_id": 1})
    u = await _users_collection().find_one({"id": user_id}, {"_id": 1})
    if not g or not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group or user not found")
    await _groups_collection().update_one({"id": group_id}, {"$pull": {"members": user_id}})
    await _users_collection().update_one({"id": user_id}, {"$pull": {"groups": group_id}})


async def list_group_policies(group_id: str, prefix: Optional[str], after: Optional[str], amount: Optional[int]) -> PolicyList:
    group = await _groups_collection().find_one({"id": group_id}, {"_id": 0, "policy_ids": 1})
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    docs = await _policies_collection().find(
        {"id": {"$in": group.get("policy_ids", [])}},
        {"_id": 0},
    ).sort("id", 1).to_list(length=None)
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


async def attach_policy_to_group(group_id: str, policy_id: str) -> None:
    g = await _groups_collection().find_one({"id": group_id}, {"_id": 1})
    p = await _policies_collection().find_one({"id": policy_id}, {"_id": 1})
    if not g:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    await _groups_collection().update_one({"id": group_id}, {"$addToSet": {"policy_ids": policy_id}})


async def detach_policy_from_group(group_id: str, policy_id: str) -> None:
    res = await _groups_collection().update_one({"id": group_id}, {"$pull": {"policy_ids": policy_id}})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")