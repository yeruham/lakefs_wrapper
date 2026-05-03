from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, constr

from .base import Pagination
from .commits import RefsDump


class Repository(BaseModel):
    id: str
    creation_date: int = Field(..., description='Unix Epoch in seconds')
    default_branch: str
    storage_id: Optional[str] = Field(
        None,
        description='Unique identifier of the underlying data store. *EXPERIMENTAL*',
    )
    storage_namespace: str = Field(
        ...,
        description='Filesystem URI to store the underlying data in (e.g. "s3://my-bucket/some/path/")',
    )
    read_only: Optional[bool] = Field(
        None,
        description='Whether the repository is a read-only repository- not relevant for bare repositories',
    )


class RepositoryMetadata(BaseModel):
    # RootModel[Optional[Dict[str, str]]]
    pass


class RepositoryMetadataSet(BaseModel):
    metadata: Dict[str, str]


class RepositoryMetadataKeys(BaseModel):
    keys: List[str]


class RepositoryList(BaseModel):
    pagination: Pagination
    results: List[Repository]


class RepositoryCreation(BaseModel):
    name: constr(pattern=r'^[a-z0-9][a-z0-9-]{2,62}$')
    storage_id: Optional[str] = Field(
        None,
        description='Unique identifier of the underlying data store. *EXPERIMENTAL*',
    )
    storage_namespace: constr(
        pattern=r'^(s3|gs|https?|mem|local|transient)://.*$'
    ) = Field(
        ...,
        description='Filesystem URI to store the underlying data in (e.g. "s3://my-bucket/some/path/")',
        example='s3://example-bucket/',
    )
    default_branch: Optional[str] = Field(None, example='main')
    sample_data: Optional[bool] = Field(False, example=True)
    read_only: Optional[bool] = Field(False, example=True)


class RepositoryDumpStatus(BaseModel):
    id: str = Field(..., description='ID of the task')
    done: bool
    update_time: str  # datetime
    error: Optional[str] = None
    refs: Optional[RefsDump] = None


class RepositoryRestoreStatus(BaseModel):
    id: str = Field(..., description='ID of the task')
    done: bool
    update_time: str  # datetime
    error: Optional[str] = None


class RepositoriesRepositoryBranchesBranchObjectsPostRequest(BaseModel):
    content: Optional[bytes] = Field(
        None, description='Only a single file per upload which must be named "content".'
    )


class RepositoriesRepositoryBranchProtectionDeleteRequest(BaseModel):
    pattern: str
