from datetime import datetime, timezone
from typing import Any, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.schemas import CreationMetadataRecord


COLLECTION = "creation_metadata"


async def save_creation_metadata(
    db: AsyncIOMotorDatabase,
    resource_type: str,
    repo_id: str,
    created_by: str,
    metadata: Optional[dict[str, Any]] = None,
    branch_name: Optional[str] = None,
    commit_id: Optional[str] = None,
    lakefs_response: Optional[dict[str, Any]] = None,
) -> CreationMetadataRecord:
    record = CreationMetadataRecord(
        resource_type=resource_type,
        repo_id=repo_id,
        branch_name=branch_name,
        commit_id=commit_id,
        created_by=created_by,
        created_at=datetime.now(timezone.utc).isoformat(),
        metadata=metadata or {},
        lakefs_response=lakefs_response,
    )
    await db[COLLECTION].insert_one(record.model_dump())
    return record


async def list_creation_metadata(
    db: AsyncIOMotorDatabase,
    repo_id: str,
    resource_type: Optional[str] = None,
    branch_name: Optional[str] = None,
    commit_id: Optional[str] = None,
    limit: int = 100,
) -> list[CreationMetadataRecord]:
    query: dict[str, Any] = {"repo_id": repo_id}
    if resource_type:
        query["resource_type"] = resource_type
    if branch_name:
        query["branch_name"] = branch_name
    if commit_id:
        query["commit_id"] = commit_id

    cursor = (
        db[COLLECTION]
        .find(query, {"_id": 0})
        .sort("created_at", -1)
        .limit(limit)
    )
    return [CreationMetadataRecord(**doc) async for doc in cursor]
