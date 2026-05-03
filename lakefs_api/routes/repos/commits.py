from .._shared import *

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
    """
    create commit
    """
    pass

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
    """
    Replay the changes from the given commit on the branch
    """
    pass



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
    """
    diff branch
    """
    pass


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
    """
    hard reset branch
    """
    pass


@app.post(
    '/repositories/{repository}/commits',
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
def create_commit_record(
    repository: str, body: CommitRecordCreation = ...
) -> Union[None, Error]:
    """
    create commit record
    """
    pass



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
    """
    get commit
    """
    pass