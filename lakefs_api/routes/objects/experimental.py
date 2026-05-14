from .._shared import *

from lakefs_api.core.lakefs_client import _client

app = APIRouter()


@app.put(
    '/repositories/{repository}/branches/{branch}/objects/stat/user_metadata',
    response_model=None,
    responses={
        '401': {'model': Error},
        '404': {'model': Error},
        '400': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects', 'experimental'],
)
def update_object_user_metadata(
    repository: str,
    branch: str = ...,
    path: str = ...,
    body: UpdateObjectUserMetadata = ...,
) -> Union[None, Error]:
    """
    rewrite (all) object metadata
    """
    pass



@app.post(
    '/repositories/{repository}/branches/{branch}/staging/pmpu',
    response_model=None,
    status_code=201,
    responses={
        '201': {'model': PresignMultipartUpload},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['experimental'],
)
def create_presign_multipart_upload(
    repository: str, branch: str = ..., path: str = ..., parts: Optional[int] = None
) -> Union[None, PresignMultipartUpload, Error]:
    """
    Initiate a multipart upload
    """
    presign_multipart_upload = _client.experimental_api.create_presign_multipart_upload(repository=repository, branch=branch, path=path, parts=parts)
    print(presign_multipart_upload)
    if presign_multipart_upload:
        return PresignMultipartUpload.model_validate(presign_multipart_upload.dict())


@app.put(
    '/repositories/{repository}/branches/{branch}/staging/pmpu/{uploadId}',
    response_model=ObjectStats,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        '409': {'model': StagingLocation},
        'default': {'model': Error},
    },
    tags=['experimental'],
)
def complete_presign_multipart_upload(
    repository: str,
    branch: str = ...,
    upload_id: str = Path(..., alias='uploadId'),
    path: str = ...,
    body: CompletePresignMultipartUpload = None,
) -> Union[ObjectStats, Error, StagingLocation]:
    """
    Complete a presign multipart upload request
    """
    return _client.experimental_api.complete_presign_multipart_upload(repository=repository, branch=branch, upload_id=upload_id, path=path, complete_presign_multipart_upload=body)


@app.delete(
    '/repositories/{repository}/branches/{branch}/staging/pmpu/{uploadId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['experimental'],
)
def abort_presign_multipart_upload(
    repository: str,
    branch: str = ...,
    upload_id: str = Path(..., alias='uploadId'),
    path: str = ...,
    body: AbortPresignMultipartUpload = None,
) -> Union[None, Error]:
    """
    Abort a presign multipart upload
    """
    return _client.experimental_api.abort_presign_multipart_upload(repository=repository, branch=branch, upload_id=upload_id, path=path, abort_presign_multipart_upload=body)


@app.put(
    '/repositories/{repository}/branches/{branch}/staging/pmpu/{uploadId}/parts/{partNumber}',
    response_model=UploadTo,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['experimental'],
)
def upload_part(
    repository: str,
    branch: str = ...,
    upload_id: str = Path(..., alias='uploadId'),
    path: str = ...,
    part_number: conint(ge=1, le=10000) = Path(..., alias='partNumber'),
    body: UploadPartFrom = ...,
) -> Union[UploadTo, Error]:
    return _client.experimental_api.upload_part(repository=repository, branch=branch, upload_id=upload_id, path=path, part_number=part_number, upload_part_from=body)


@app.put(
    '/repositories/{repository}/branches/{branch}/staging/pmpu/{uploadId}/parts/{partNumber}/copy',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['experimental'],
)
def upload_part_copy(
    repository: str,
    branch: str = ...,
    upload_id: str = Path(..., alias='uploadId'),
    path: str = ...,
    part_number: conint(ge=1, le=10000) = Path(..., alias='partNumber'),
    body: UploadPartCopyFrom = ...,
) -> Union[None, Error]:
    pass