from fastapi import APIRouter

app = APIRouter()


@app.get(
    '/repositories/{repository}/metadata/meta_range/{meta_range}',
    response_model=StorageURI,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['metadata'],
)
def get_meta_range(repository: str, meta_range: str = ...) -> Union[StorageURI, Error]:
    """
    return URI to a meta-range file
    """
    pass


@app.get(
    '/repositories/{repository}/metadata/object/{type}/{object_id}',
    response_model=bytes,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def get_metadata_object(
    presign: Optional[bool] = None,
    repository: str = ...,
    object_id: str = ...,
    type: Type6 = ...,
) -> Union[bytes, Error]:
    """
    return a lakeFS metadata object by ID
    """
    pass


@app.get(
    '/repositories/{repository}/metadata/range/{range}',
    response_model=StorageURI,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['metadata'],
)
def get_range(repository: str, range: str = ...) -> Union[StorageURI, Error]:
    """
    return URI to a range file
    """
    pass
