from .._shared import *
from ...lakefs_client import _client

app = APIRouter()

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
    return _client.staging_api.get_physical_address(repository=repository, branch=branch, presign=presign, path=path)


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
    raise NotImplementedError