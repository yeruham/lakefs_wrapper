from .._shared import *
from lakefs_api.core.lakefs_client import _client

app = APIRouter()


@app.get(
    '/repositories',
    response_model=RepositoryList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
async def list_repositories(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    search: Optional[str] = None,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[RepositoryList, Error]:
    # await require_permission(current_user.username, LakeFSAction.read, "*")
    return _client.repositories_api.list_repositories(prefix=prefix, after=after, amount=amount, search=search)


@app.post(
    '/repositories',
    response_model=None,
    status_code=201,
    responses={
        '201': {'model': Repository},
        '400': {'model': Error},
        '401': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
async def create_repository(
    bare: Optional[bool] = False,
    body: RepositoryCreation = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[None, Repository, Error]:
    repo = _client.repositories_api.create_repository(repository_creation=body, bare=bare)
    if repo:
        return Repository.model_validate(repo.dict())


@app.get(
    '/repositories/{repository}',
    response_model=Repository,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
async def get_repository(
    repository: str,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[Repository, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.repositories_api.get_repository(repository=repository)


@app.delete(
    '/repositories/{repository}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def delete_repository(
    force: Optional[bool] = False, repository: str = ...
) -> Union[None, Error]:
    raise NotImplementedError


@app.get(
    '/repositories/{repository}/metadata',
    response_model=RepositoryMetadata,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
async def get_repository_metadata(
    repository: str,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[RepositoryMetadata, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.repositories_api.get_repository(repository=repository)


@app.post(
    '/repositories/{repository}/metadata',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def set_repository_metadata(
    repository: str, body: RepositoryMetadataSet = ...
) -> Union[None, Error]:
    raise NotImplementedError


@app.delete(
    '/repositories/{repository}/metadata',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def delete_repository_metadata(
    repository: str, body: RepositoryMetadataKeys = ...
) -> Union[None, Error]:
    raise NotImplementedError
