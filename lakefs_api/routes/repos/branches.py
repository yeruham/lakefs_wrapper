from .._shared import *
from ...lakefs_client import _client

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
def list_branches(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    show_hidden: Optional[bool] = False,
    repository: str = ...,
) -> Union[RefList, Error]:
    return _client.branches_api.list_branches(repository=repository, prefix=prefix, after=after, amount=amount, show_hidden=show_hidden)


@app.post(
    '/repositories/{repository}/branches',
    response_model=None,
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
def create_branch(
    repository: str, body: BranchCreation = ...
) -> Union[None, str, Error]:
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
def get_branch(repository: str, branch: str = ...) -> Union[Ref, Error]:
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
def delete_branch(
    force: Optional[bool] = False, repository: str = ..., branch: str = ...
) -> Union[None, Error]:
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
def reset_branch(
    repository: str, branch: str = ..., body: ResetCreation = ...
) -> Union[None, Error]:
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
def revert_branch(
    repository: str, branch: str = ..., body: RevertCreation = ...
) -> Union[None, Error]:
    return _client.branches_api.revert_branch(repository=repository, branch=branch, revert_creation=body)