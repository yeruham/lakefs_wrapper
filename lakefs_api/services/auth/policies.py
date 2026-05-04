from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import HTTPException, status

from ...core.database import _policies_collection
from utils import _now_ts, _paginate
from lakefs_api.models import Pagination, Policy, PolicyList



async def list_policies(prefix: Optional[str], after: Optional[str], amount: Optional[int]) -> PolicyList:
    query: dict[str, Any] = {}
    if prefix:
        query["id"] = {"$regex": f"^{prefix}"}
    docs = await _policies_collection().find(query, {"_id": 0}).sort("id", 1).to_list(length=None)
    policies = [Policy.model_validate(d) for d in docs]
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


async def create_policy(body: Policy) -> Policy:
    exists = await _policies_collection().find_one({"id": body.id}, {"_id": 1})
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Policy already exists")
    doc = body.model_dump()
    doc.setdefault("creation_date", _now_ts())
    await _policies_collection().insert_one(doc)
    return Policy.model_validate(doc)


async def get_policy(policy_id: str) -> Policy:
    doc = await _policies_collection().find_one({"id": policy_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return Policy.model_validate(doc)


async def update_policy(policy_id: str, body: Policy) -> Policy:
    doc = body.model_dump(exclude_unset=True)
    doc.pop("id", None)
    res = await _policies_collection().update_one({"id": policy_id}, {"$set": doc})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    updated = await _policies_collection().find_one({"id": policy_id}, {"_id": 0})
    return Policy.model_validate(updated)


async def delete_policy(policy_id: str) -> None:
    res = await _policies_collection().delete_one({"id": policy_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
