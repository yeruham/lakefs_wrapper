"""Group & permission CRUD operations against MongoDB."""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.schemas import GroupCreate, GroupInDB, GroupUpdate, Permission

COLLECTION = "groups"


async def get_group(db: AsyncIOMotorDatabase, group_name: str) -> Optional[GroupInDB]:
    doc = await db[COLLECTION].find_one({"group_name": group_name}, {"_id": 0})
    if doc:
        return GroupInDB(**doc)
    return None


async def create_group(db: AsyncIOMotorDatabase, payload: GroupCreate) -> GroupInDB:
    existing = await get_group(db, payload.group_name)
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="Group already exists")
    group = GroupInDB(group_name=payload.group_name, permissions=payload.permissions)
    await db[COLLECTION].insert_one(group.model_dump())
    return group


async def list_groups(db: AsyncIOMotorDatabase) -> list[GroupInDB]:
    cursor = db[COLLECTION].find({}, {"_id": 0})
    return [GroupInDB(**doc) async for doc in cursor]


async def update_group_permissions(
    db: AsyncIOMotorDatabase, group_name: str, payload: GroupUpdate
) -> Optional[GroupInDB]:
    await db[COLLECTION].update_one(
        {"group_name": group_name},
        {"$set": {"permissions": [p.model_dump() for p in payload.permissions]}},
    )
    return await get_group(db, group_name)


async def delete_group(db: AsyncIOMotorDatabase, group_name: str) -> bool:
    result = await db[COLLECTION].delete_one({"group_name": group_name})
    return result.deleted_count > 0


# ── RBAC check helper (used by controllers) ───────────────────────────────────

async def user_can(
    db: AsyncIOMotorDatabase,
    user_groups: list[str],
    repo: str,
    action: str,          # "can_read" | "can_write" | "can_merge"
) -> bool:
    """Return True if any of the user's groups grant the requested action on repo."""
    cursor = db[COLLECTION].find({"group_name": {"$in": user_groups}}, {"_id": 0})
    async for doc in cursor:
        group = GroupInDB(**doc)
        for perm in group.permissions:
            if perm.repo == repo and getattr(perm, action, False):
                return True
    return False
