"""User CRUD operations against MongoDB."""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.schemas import UserCreate, UserInDB, UserUpdate, UserPublic
from app.core.security import hash_password


COLLECTION = "users"


async def get_user(db: AsyncIOMotorDatabase, username: str) -> Optional[UserInDB]:
    doc = await db[COLLECTION].find_one({"username": username})
    if doc:
        return UserInDB(**doc)
    return None


async def create_user(db: AsyncIOMotorDatabase, payload: UserCreate) -> UserPublic:
    existing = await get_user(db, payload.username)
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="Username already exists")
    user = UserInDB(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        groups=payload.groups,
    )
    await db[COLLECTION].insert_one(user.model_dump())
    return UserPublic(username=user.username, groups=user.groups, is_active=user.is_active)


async def list_users(db: AsyncIOMotorDatabase) -> list[UserPublic]:
    cursor = db[COLLECTION].find({}, {"hashed_password": 0, "_id": 0})
    return [UserPublic(**doc) async for doc in cursor]


async def update_user(db: AsyncIOMotorDatabase, username: str, payload: UserUpdate) -> Optional[UserPublic]:
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        return await get_user(db, username)
    await db[COLLECTION].update_one({"username": username}, {"$set": update_data})
    return await get_user(db, username)


async def delete_user(db: AsyncIOMotorDatabase, username: str) -> bool:
    result = await db[COLLECTION].delete_one({"username": username})
    return result.deleted_count > 0
