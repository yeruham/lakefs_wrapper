from .._shared import *
from lakefs_api.core.lakefs_client import _client

app = APIRouter()


@app.get(
    '/repositories/{repository}/tags',
    response_model=RefList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['tags'],
)
async def list_tags(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    repository: str = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[RefList, Error]:
    # await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.tags_api.list_tags(repository=repository, prefix=prefix, after=after, amount=amount)


@app.post(
    '/repositories/{repository}/tags',
    response_model=None,
    status_code=201,
    responses={
        '201': {'model': Ref},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['tags'],
)
async def create_tag(
    repository: str,
    body: TagCreation = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[None, Ref, Error]:
    # await require_permission(current_user.username, LakeFSAction.write, repository)
    return _client.tags_api.create_tag(repository=repository, tag_creation=body)


@app.get(
    '/repositories/{repository}/tags/{tag}',
    response_model=Ref,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['tags'],
)
async def get_tag(
    repository: str,
    tag: str = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[Ref, Error]:
    # await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.tags_api.get_tag(repository=repository, tag=tag)


@app.delete(
    '/repositories/{repository}/tags/{tag}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['tags'],
)
async def delete_tag(
    force: Optional[bool] = None,
    repository: str = ...,
    tag: str = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[None, Error]:
    # await require_permission(current_user.username, LakeFSAction.delete, repository)
    return _client.tags_api.delete_tag(repository=repository, tag=tag, force=force)
