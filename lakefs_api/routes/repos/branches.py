from .._shared import *
from lakefs_api.core.lakefs_client import _client

app = APIRouter()


@app.get(
    '/repositories/{repository}/branches',
    response_model=RefList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
async def list_branches(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    show_hidden: Optional[bool] = False,
    repository: str = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[RefList, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.branches_api.list_branches(repository=repository, prefix=prefix, after=after, amount=amount, show_hidden=show_hidden)


@app.post(
    '/repositories/{repository}/branches',
    response_model=None,
    status_code=201,
    responses={
        '201': {'model': str},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
async def create_branch(
    repository: str,
    body: BranchCreation = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[None, str, Error]:
    await require_permission(current_user.username, LakeFSAction.write, repository)
    return _client.branches_api.create_branch(repository, body)


@app.get(
    '/repositories/{repository}/branches/{branch}',
    response_model=Ref,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
async def get_branch(
    repository: str,
    branch: str = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[Ref, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.branches_api.get_branch(repository=repository, branch=branch)


@app.delete(
    '/repositories/{repository}/branches/{branch}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
async def delete_branch(
    force: Optional[bool] = False,
    repository: str = ...,
    branch: str = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[None, Error]:
    await require_permission(current_user.username, LakeFSAction.delete, repository)
    return _client.branches_api.delete_branch(repository=repository, branch=branch, force=force)


@app.put(
    '/repositories/{repository}/branches/{branch}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
async def reset_branch(
    repository: str,
    branch: str = ...,
    body: ResetCreation = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[None, Error]:
    await require_permission(current_user.username, LakeFSAction.write, repository)
    return _client.branches_api.reset_branch(repository=repository, branch=branch, reset_creation=body)


@app.post(
    '/repositories/{repository}/branches/{branch}/revert',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
async def revert_branch(
    repository: str,
    branch: str = ...,
    body: RevertCreation = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[None, Error]:
    await require_permission(current_user.username, LakeFSAction.write, repository)
    return _client.branches_api.revert_branch(repository=repository, branch=branch, revert_creation=body)


@app.get(
    '/repositories/{repository}/branches/{branch}/diff',
    response_model=DiffList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
async def diff_branch(
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    prefix: Optional[str] = None,
    delimiter: Optional[str] = None,
    repository: str = ...,
    branch: str = ...,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[DiffList, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.branches_api.diff_branch(repository=repository, branch=branch, prefix=prefix, amount=amount, after=after, delimiter=delimiter)
