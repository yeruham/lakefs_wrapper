from fastapi import APIRouter

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
    """
    list branches
    """
    pass


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
    """
    create branch
    """
    pass


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
    """
    get branch
    """
    pass


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
    """
    delete branch
    """
    pass


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
    """
    reset branch
    """
    pass



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
    """
    revert
    """
    pass