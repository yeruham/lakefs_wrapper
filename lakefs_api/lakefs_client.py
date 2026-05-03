import lakefs_sdk
from lakefs_sdk.client import LakeFSClient

from lakefs_api.core.config import get_settings

settings = get_settings()


def _get_client() -> LakeFSClient:
    cfg = lakefs_sdk.Configuration(
        host=settings.lakefs_endpoint,
        username=settings.lakefs_access_key,
        password=settings.lakefs_secret_key,
    )
    return LakeFSClient(configuration=cfg)

_client = _get_client()