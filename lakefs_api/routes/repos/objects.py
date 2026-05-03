from .._shared import *

app = APIRouter()


@app.put(
    '/repositories/{repository}/branches/{branch}/objects',
    response_model=None,
    responses={
        '201': {'model': ObjectStats},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def stage_object(
    repository: str, branch: str = ..., path: str = ..., body: ObjectStageCreation = ...
) -> Union[None, ObjectStats, Error]:
    """
    stage an object's metadata for the given branch
    """
    pass


@app.post(
    '/repositories/{repository}/branches/{branch}/objects',
    response_model=None,
    responses={
        '201': {'model': ObjectStats},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '412': {'model': Error},
        '501': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def upload_object(
    if__none__match: Optional[str] = Header(None, alias='If-None-Match'),
    if__match: Optional[str] = Header(None, alias='If-Match'),
    storage_class: Optional[str] = Query(None, alias='storageClass'),
    force: Optional[bool] = False,
    repository: str = ...,
    branch: str = ...,
    path: str = ...,
    file: bytes = b'',
) -> Union[None, ObjectStats, Error]:
    pass


@app.delete(
    '/repositories/{repository}/branches/{branch}/objects',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def delete_object(
    force: Optional[bool] = False,
    no_tombstone: Optional[bool] = False,
    repository: str = ...,
    branch: str = ...,
    path: str = ...,
) -> Union[None, Error]:
    """
    delete object. Missing objects will not return a NotFound error.
    """
    pass


@app.post(
    '/repositories/{repository}/branches/{branch}/objects/copy',
    response_model=None,
    responses={
        '201': {'model': ObjectStats},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def copy_object(
    repository: str,
    branch: str = ...,
    dest_path: str = ...,
    body: ObjectCopyCreation = ...,
) -> Union[None, ObjectStats, Error]:
    """
    create a copy of an object
    """
    pass


@app.post(
    '/repositories/{repository}/branches/{branch}/objects/delete',
    response_model=ObjectErrorList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def delete_objects(
    repository: str,
    branch: str = ...,
    force: Optional[bool] = False,
    no_tombstone: Optional[bool] = False,
    body: PathList = ...,
) -> Union[ObjectErrorList, Error]:
    """
    delete objects. Missing objects will not return a NotFound error.
    """
    pass


@app.get(
    '/repositories/{repository}/branches/{branch}/objects/stage_allowed',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def upload_object_preflight(
    repository: str, branch: str = ..., path: str = ...
) -> Union[None, Error]:
    pass


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


@app.get(
    '/repositories/{repository}/branches/{branch}/staging/backing',
    response_model=StagingLocation,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['staging'],
)
def get_physical_address(
    presign: Optional[bool] = None,
    repository: str = ...,
    branch: str = ...,
    path: str = ...,
) -> Union[StagingLocation, Error]:
    """
    generate an address to which the client can upload an object
    """
    pass


@app.put(
    '/repositories/{repository}/branches/{branch}/staging/backing',
    response_model=ObjectStats,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': StagingLocation},
        '412': {'model': Error},
        '501': {'model': Error},
        'default': {'model': Error},
    },
    tags=['staging'],
)
def link_physical_address(
    if__none__match: Optional[str] = Header(None, alias='If-None-Match'),
    if__match: Optional[str] = Header(None, alias='If-Match'),
    repository: str = ...,
    branch: str = ...,
    path: str = ...,
    body: StagingMetadata = ...,
) -> Union[ObjectStats, Error, StagingLocation]:
    """
    associate staging on this physical address with a path
    """
    pass



@app.post(
    '/repositories/{repository}/branches/{branch}/staging/pmpu',
    response_model=None,
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
    pass


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
    pass


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
    pass


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
    pass


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