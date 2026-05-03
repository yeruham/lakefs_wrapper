from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, RootModel, Field

from .auth import ExternalPrincipalSettings


class StorageConfig(BaseModel):
    blockstore_type: str
    blockstore_namespace_example: str
    blockstore_namespace_ValidityRegex: str
    default_namespace_prefix: Optional[str] = None
    pre_sign_support: bool
    pre_sign_support_ui: bool
    import_support: bool
    import_validity_regex: str
    pre_sign_multipart_upload: Optional[bool] = None
    blockstore_id: Optional[str] = None
    blockstore_description: Optional[str] = None


class StorageConfigList(RootModel[List[StorageConfig]]):
    pass


class VersionConfig(BaseModel):
    version: Optional[str] = None
    version_context: Optional[str] = None
    latest_version: Optional[str] = None
    upgrade_recommended: Optional[bool] = None
    upgrade_url: Optional[str] = None


class CustomViewer(BaseModel):
    name: str
    url: str
    extensions: Optional[List[str]] = None
    content_types: Optional[List[str]] = None


class CapabilitiesConfig(BaseModel):
    pass


class UIConfig(BaseModel):
    custom_viewers: Optional[List[CustomViewer]] = None


class Config(BaseModel):
    version_config: Optional[VersionConfig] = None
    storage_config: Optional[StorageConfig] = None
    storage_config_list: Optional[StorageConfigList] = None
    ui_config: Optional[UIConfig] = None
    capabilities_config: Optional[CapabilitiesConfig] = None


class StatsEvent(BaseModel):
    class_: str = Field(
        ...,
        alias='class',
        description='stats event class (e.g. "s3_gateway", "openapi_request", "experimental-feature", "ui-event")',
    )
    name: str = Field(
        ...,
        description='stats event name (e.g. "put_object", "create_repository", "<experimental-feature-name>")',
    )
    count: int = Field(..., description='number of events of the class and name')


class StatsEventsList(BaseModel):
    events: List[StatsEvent]


class UsageReport(BaseModel):
    year: int
    month: int
    count: int


class InstallationUsageReport(BaseModel):
    installation_id: str
    reports: List[UsageReport]
