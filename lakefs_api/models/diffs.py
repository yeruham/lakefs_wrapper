from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .base import Pagination
from .commits import Commit, CommitCreation
from .objects import ObjectUserMetadata


class DiffComparisonType(Enum):
    """Diff comparison type (two_dot vs three_dot). Codegen produces Type3 and Type4."""
    two_dot = 'two_dot'
    three_dot = 'three_dot'


# Aliases matching the generated names
Type3 = DiffComparisonType
Type4 = DiffComparisonType


class RangeType(Enum):
    """Range metadata type. Codegen produces Type5 and Type6."""
    range = 'range'
    meta_range = 'meta_range'


# Aliases matching the generated names
Type5 = RangeType
Type6 = RangeType


class DiffType(Enum):
    added = 'added'
    removed = 'removed'
    changed = 'changed'
    conflict = 'conflict'
    prefix_changed = 'prefix_changed'


class DiffPathType(Enum):
    common_prefix = 'common_prefix'
    object = 'object'


class DiffObjectStat(BaseModel):
    checksum: str
    mtime: int = Field(..., description='Unix Epoch in seconds')
    content_type: str = Field(..., description='Object media type')
    metadata: Optional[ObjectUserMetadata] = None


class Diff(BaseModel):
    type: DiffType
    path: str
    path_type: DiffPathType
    size_bytes: Optional[int] = Field(
        None, description='represents the size of the added/changed/deleted entry'
    )
    right: Optional[DiffObjectStat] = Field(
        None, description='ObjectStats of the right side of the diff.'
    )


class DiffList(BaseModel):
    pagination: Pagination
    results: List[Diff]


class BranchProtectionRule(BaseModel):
    pattern: str = Field(
        ...,
        description='fnmatch pattern for the branch name, supporting * and ? wildcards',
        example='stable_*',
    )


class ImportLocationType(Enum):
    common_prefix = 'common_prefix'
    object = 'object'


class ImportLocation(BaseModel):
    type: ImportLocationType = Field(
        ..., description="Path type, can either be 'common_prefix' or 'object'"
    )
    path: str = Field(
        ...,
        description="A source location to a 'common_prefix' or to a single object.",
        example='s3://my-bucket/production/collections/',
    )
    destination: str = Field(
        ...,
        description="Destination for the imported objects on the branch.",
        example='collections/',
    )


class ImportCreation(BaseModel):
    paths: List[ImportLocation]
    commit: CommitCreation
    force: Optional[bool] = False


class ImportStatus(BaseModel):
    completed: bool
    update_time: datetime
    ingested_objects: Optional[int] = Field(
        None, description='Number of objects processed so far'
    )
    metarange_id: Optional[str] = None
    commit: Optional[Commit] = None
    error: Optional['Error'] = None


class ImportCreationResponse(BaseModel):
    id: str = Field(..., description='The id of the import process')


class RangeMetadata(BaseModel):
    id: str = Field(..., description='ID of the range.', example='480e19972a6...')
    min_key: str = Field(..., description='First key in the range.')
    max_key: str = Field(..., description='Last key in the range.')
    count: int = Field(..., description='Number of records in the range.')
    estimated_size: int = Field(..., description='Estimated size of the range in bytes')


class MetaRangeCreation(BaseModel):
    ranges: List[RangeMetadata] = Field(..., min_length=1)


class MetaRangeCreationResponse(BaseModel):
    id: Optional[str] = Field(None, description='The id of the created metarange')


class GarbageCollectionConfig(BaseModel):
    grace_period: Optional[int] = Field(
        None,
        description='Duration in seconds. Objects created in the recent grace_period will not be collected.',
    )


class GarbageCollectionRule(BaseModel):
    branch_id: str
    retention_days: int


class GarbageCollectionRules(BaseModel):
    default_retention_days: int
    branches: List[GarbageCollectionRule]


class GarbageCollectionPrepareResponse(BaseModel):
    run_id: str = Field(..., description='a unique identifier generated for this GC job')
    gc_commits_location: str = Field(
        ..., description='location of the resulting commits csv table (partitioned by run_id)'
    )
    gc_addresses_location: str = Field(
        ..., description='location to use for expired addresses parquet table (partitioned by run_id)'
    )
    gc_commits_presigned_url: Optional[str] = Field(
        None, description='a presigned url to download the commits csv'
    )


class PrepareGarbageCollectionCommitsStatus(BaseModel):
    task_id: str = Field(..., description='the id of the task preparing the GC commits')
    completed: bool = Field(
        ...,
        description='true if the task has completed (either successfully or with an error)',
    )
    update_time: datetime = Field(..., description='last time the task status was updated')
    result: Optional[GarbageCollectionPrepareResponse] = None
    error: Optional['Error'] = None


class PrepareGCUncommittedRequest(BaseModel):
    continuation_token: Optional[str] = None


class PrepareGCUncommittedResponse(BaseModel):
    run_id: str
    gc_uncommitted_location: str = Field(
        ..., description='location of uncommitted information data'
    )
    continuation_token: Optional[str] = None


class ActionRunStatus(Enum):
    failed = 'failed'
    completed = 'completed'


class ActionRun(BaseModel):
    run_id: str
    branch: str
    start_time: datetime
    end_time: Optional[datetime] = None
    event_type: str
    status: ActionRunStatus
    commit_id: str


class ActionRunList(BaseModel):
    pagination: Pagination
    results: List[ActionRun]


class HookRun(BaseModel):
    hook_run_id: str
    action: str
    hook_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: ActionRunStatus


class HookRunList(BaseModel):
    pagination: Pagination
    results: List[HookRun]


class TaskInfo(BaseModel):
    id: str = Field(..., description='ID of the task')


class TaskCreation(BaseModel):
    id: str = Field(..., description='The id of the new task')


# Forward reference for Error
from .errors import Error  # noqa: E402
ImportStatus.model_rebuild()
PrepareGarbageCollectionCommitsStatus.model_rebuild()
