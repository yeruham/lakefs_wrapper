from .._shared import *
from ...lakefs_client import _client

app = APIRouter()


@app.post(
    '/repositories/{repository}/branches/{branch}/commits',
    response_model=None,
    responses={
        '201': {'model': Commit},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        '412': {'model': Error},
        'default': {'model': Error},
    },
    tags=['commits'],
)
def commit(
    source_metarange: Optional[str] = None,
    repository: str = ...,
    branch: str = ...,
    body: CommitCreation = ...,
) -> Union[None, Commit, Error]:
    return _client.commits_api.commit(repository=repository, branch=branch, source_metarange=source_metarange, commit_creation=body)

@app.post(
    '/repositories/{repository}/branches/{branch}/cherry-pick',
    response_model=None,
    responses={
        '201': {'model': Commit},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['branches'],
)
def cherry_pick(
    repository: str, branch: str = ..., body: CherryPickCreation = ...
) -> Union[None, Commit, Error]:
    raise NotImplementedError



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
def diff_branch(
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    prefix: Optional[str] = None,
    delimiter: Optional[str] = None,
    repository: str = ...,
    branch: str = ...,
) -> Union[DiffList, Error]:
    return _client.branches_api.diff_branch(repository=repository, branch=branch, prefix=prefix, amount=amount, after=after, delimiter=delimiter)


@app.put(
    '/repositories/{repository}/branches/{branch}/hard_reset',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['experimental'],
)
def hard_reset_branch(
    ref: str, force: Optional[bool] = False, repository: str = ..., branch: str = ...
) -> Union[None, Error]:
    raise NotImplementedError


@app.get(
    '/repositories/{repository}/commits/{commitId}',
    response_model=Commit,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['commits'],
)
def get_commit(
    repository: str, commit_id: str = Path(..., alias='commitId')
) -> Union[Commit, Error]:
    return _client.commits_api.get_commit(repository=repository, commit_id=commit_id)