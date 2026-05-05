from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import get_settings
from lakefs_api.models import Policy
from lakefs_api.services.auth.schemas import GroupInDB, UserInDB


settings = get_settings()

_client: AsyncIOMotorClient | None = None


async def connect_db() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.mongo_uri)
    # Ping to verify connectivity at startup
    await _client.admin.command("ping")


async def close_db() -> None:
    global _client
    if _client:
        _client.close()


def _get_db() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("Database not initialised – call connect_db() first")
    return _client[settings.mongo_db_name]


def _groups_collection():
    return _get_db()["auth_groups"]


def _users_collection():
    return _get_db()["auth_users"]


def _policies_collection():
    return _get_db()["auth_policies"]


async def get_user_by_id(user_id: str) -> UserInDB | None:
    doc = await _users_collection().find_one({"id": user_id}, {"_id": 0})
    if doc is None:
        return None
    return UserInDB(**doc)


async def get_groups_by_ids(group_ids: list[str]) -> list[GroupInDB]:
    if not group_ids:
        return []
    cursor = _groups_collection().find(
        {"id": {"$in": group_ids}},
        {"policy_ids": 1, "_id": 0},
    )
    docs = await cursor.to_list(length=None)
    return [GroupInDB(**doc) for doc in docs]


async def get_policies_by_ids(policy_ids: list[str]) -> list[Policy]:
    if not policy_ids:
        return []
    cursor = _policies_collection().find({"id": {"$in": policy_ids}}, {"_id": 0})
    docs = await cursor.to_list(length=None)
    return [Policy(**doc) for doc in docs]