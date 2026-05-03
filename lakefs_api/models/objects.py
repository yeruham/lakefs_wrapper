from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, RootModel, constr

from .base import Pagination


class PathType(Enum):
    common_prefix = 'common_prefix'
    object = 'object'


class ObjectUserMetadata(RootModel[Optional[Dict[str, str]]]):
    pass


class UnderlyingObjectProperties(BaseModel):
    storage_class: Optional[str] = None


class ObjectCopyCreation(BaseModel):
    src_path: str = Field(
        ..., description='path of the copied object relative to the ref'
    )
    src_ref: Optional[str] = Field(
        None, description='a reference, if empty uses the provided branch as ref'
    )
    force: Optional[bool] = False
    shallow: Optional[bool] = Field(
        False,
        description=(
            'Create a shallow copy of the object (without copying the actual data). '
            'At the moment shallow copy only works for same repository and branch.\n'
            'Please note that shallow copied objects might be in contention with garbage '
            'collection and branch retention policies - use with caution.\n'
        ),
    )


class ObjectStats(BaseModel):
    path: str
    path_type: PathType
    physical_address: str = Field(
        ...,
        description=(
            'The location of the object on the underlying object store.\n'
            'Formatted as a native URI with the object store type as scheme ("s3://...", "gs://...", etc.)\n'
            'Or, in the case of presign=true, will be an HTTP URL to be consumed via regular HTTP GET\n'
        ),
    )
    physical_address_expiry: Optional[int] = Field(
        None,
        description=(
            'If present and nonzero, physical_address is a pre-signed URL and\n'
            'will expire at this Unix Epoch time.\n\nThis field is *optional*.\n'
        ),
    )
    checksum: str
    size_bytes: Optional[int] = Field(
        None,
        description='The number of bytes in the object. This field is optional for the client to supply.',
    )
    mtime: int = Field(..., description='Unix Epoch in seconds')
    metadata: Optional[ObjectUserMetadata] = None
    content_type: Optional[str] = Field(None, description='Object media type')


class ObjectStatsList(BaseModel):
    pagination: Pagination
    results: List[ObjectStats]


class UpdateObjectUserMetadata(BaseModel):
    set: ObjectUserMetadata = Field(..., description='Set this object user metadata')


class ObjectStageCreation(BaseModel):
    physical_address: str
    checksum: str
    size_bytes: int
    mtime: Optional[int] = Field(None, description='Unix Epoch in seconds')
    metadata: Optional[ObjectUserMetadata] = None
    content_type: Optional[str] = Field(None, description='Object media type')
    force: Optional[bool] = False


class PathList(BaseModel):
    paths: List[str]


class StagingLocation(BaseModel):
    physical_address: Optional[str] = None
    presigned_url: Optional[str] = Field(
        None,
        description='if presign=true is passed in the request, this field will contain a pre-signed URL to use when uploading',
    )
    presigned_url_expiry: Optional[int] = Field(
        None,
        description='If present and nonzero, physical_address is a pre-signed URL and will expire at this Unix Epoch time.\n\nThis field is *optional*.\n',
    )


class StagingMetadata(BaseModel):
    staging: StagingLocation
    checksum: str = Field(
        ...,
        description='unique identifier of object content on backing store (typically ETag)',
    )
    size_bytes: int
    user_metadata: Optional[Dict[str, str]] = None
    content_type: Optional[str] = Field(None, description='Object media type')
    mtime: Optional[int] = Field(
        None, description='Unix Epoch in seconds.  May be ignored by server.'
    )
    force: Optional[bool] = False


class StorageURI(BaseModel):
    location: str


class PresignMultipartUpload(BaseModel):
    upload_id: str
    physical_address: str
    presigned_urls: Optional[List[str]] = None


class UploadPart(BaseModel):
    part_number: int
    etag: str


class UploadPartFrom(BaseModel):
    physical_address: str = Field(
        ...,
        description='The physical address (of the entire intended object) returned from\ncreatePresignMultipartUpload.\n',
    )


class CopyPartSource(BaseModel):
    repository: str
    ref: str
    path: str
    range: Optional[constr(pattern=r'^bytes=((\d*-\d*,? ?)+)$')] = Field(
        None, description='Range of bytes to copy'
    )


class UploadPartCopyFrom(UploadPartFrom):
    copy_source: CopyPartSource = Field(..., description='Source of copy')


class UploadTo(BaseModel):
    presigned_url: str


class CompletePresignMultipartUpload(BaseModel):
    physical_address: str
    parts: List[UploadPart] = Field(
        ...,
        description='List of uploaded parts, should be ordered by ascending part number',
    )
    user_metadata: Optional[Dict[str, str]] = None
    content_type: Optional[str] = Field(None, description='Object media type')


class AbortPresignMultipartUpload(BaseModel):
    physical_address: str


class UpdateToken(BaseModel):
    staging_token: str
