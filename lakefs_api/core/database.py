from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import get_settings

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
