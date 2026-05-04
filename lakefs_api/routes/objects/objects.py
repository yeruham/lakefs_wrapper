from .._shared import *
from ...lakefs_client import _client

app = APIRouter()


@app.head(
    '/repositories/{repository}/refs/{ref}/objects',
    response_model=None,
    tags=['objects'],
)
def head_object(
    range: Optional[constr(pattern=r'^bytes=((\d*-\d*,? ?)+)$')] = Header(
        None, alias='Range'
    ),
    repository: str = ...,
    ref: str = ...,
    path: str = ...,
) -> None:
    return _client.objects_api.head_object(repository=repository, ref=ref, range=range, path=path)


@app.get(
    '/repositories/{repository}/refs/{ref}/objects/ls',
    response_model=ObjectStatsList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def list_objects(
    repository: str,
    ref: str = ...,
    user_metadata: Optional[bool] = True,
    presign: Optional[bool] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    delimiter: Optional[str] = None,
    prefix: Optional[str] = None,
) -> Union[ObjectStatsList, Error]:
    return _client.objects_api.list_objects(repository=repository, ref=ref, user_metadata=user_metadata, presign=presign, after=after, amount=amount, delimiter=delimiter, prefix=prefix)


@app.get(
    '/repositories/{repository}/refs/{ref}/objects/stat',
    response_model=ObjectStats,
    responses={
        '401': {'model': Error},
        '404': {'model': Error},
        '400': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def stat_object(
    repository: str,
    ref: str = ...,
    path: str = ...,
    user_metadata: Optional[bool] = True,
    presign: Optional[bool] = None,
) -> Union[ObjectStats, Error]:
    return _client.objects_api.stat_object(repository=repository, ref=ref, path=path, user_metadata=user_metadata, presign=presign)

@app.post(
    '/repositories/{repository}/branches/{branch}/objects',
    response_model=None,
    status_code=201,
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
    return _client.objects_api.upload_object(repository=repository, branch=branch, path=path, force=force, storage_class=storage_class, if_none_match=if__none__match, if_match=if__match, content=file)


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
    return _client.objects_api.delete_object(repository=repository, branch=branch, path=path, force=force, no_tombstone=no_tombstone)


@app.post(
    '/repositories/{repository}/branches/{branch}/objects/copy',
    response_model=None,
    status_code=201,
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
    return _client.objects_api.copy_object(repository=repository, branch=branch, dest_path=dest_path, object_copy_creation=body)


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
    return _client.objects_api.delete_objects(repository=repository, branch=branch, force=force, no_tombstone=no_tombstone, path_list=body)


@app.get(
    '/repositories/{repository}/refs/{ref}/objects',
    response_model=bytes,
    responses={
        '206': {'model': bytes},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        '410': {'model': Error},
        '416': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def get_object(
    range: Optional[constr(pattern=r'^bytes=((\d*-\d*,? ?)+)$')] = Header(
        None, alias='Range'
    ),
    if__none__match: Optional[str] = Header(None, alias='If-None-Match'),
    presign: Optional[bool] = None,
    repository: str = ...,
    ref: str = ...,
    path: str = ...,
) -> Union[bytes, Error]:
    return _client.objects_api.get_object(repository=repository, ref=ref, path=path, presign=presign, range=range, if_none_match=if__none__match)