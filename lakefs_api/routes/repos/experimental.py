from .._shared import *

app = APIRouter()


@app.get(
    '/repositories/{repository}/pulls',
    response_model=PullRequestsList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['pulls', 'experimental'],
)
def list_pull_requests(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    status: Optional[Status4] = 'all',
    repository: str = ...,
) -> Union[PullRequestsList, Error]:
    """
    list pull requests
    """
    pass


@app.post(
    '/repositories/{repository}/pulls',
    response_model=None,
    responses={
        '201': {'model': PullRequestCreationResponse},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['pulls', 'experimental'],
)
def create_pull_request(
    repository: str, body: PullRequestCreation = ...
) -> Union[None, PullRequestCreationResponse, Error]:
    """
    create pull request
    """
    pass


@app.get(
    '/repositories/{repository}/pulls/{pull_request}',
    response_model=PullRequest,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['pulls', 'experimental'],
)
def get_pull_request(
    repository: str, pull_request: str = ...
) -> Union[PullRequest, Error]:
    """
    get pull request
    """
    pass


@app.patch(
    '/repositories/{repository}/pulls/{pull_request}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['pulls', 'experimental'],
)
def update_pull_request(
    repository: str, pull_request: str = ..., body: PullRequestBasic = ...
) -> Union[None, Error]:
    """
    update pull request
    """
    pass


@app.put(
    '/repositories/{repository}/pulls/{pull_request}/merge',
    response_model=MergeResult,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': MergeResult},
        '412': {'model': Error},
        'default': {'model': Error},
    },
    tags=['pulls', 'experimental'],
)
def merge_pull_request(
    repository: str, pull_request: str = ...
) -> Union[MergeResult, Error]:
    """
    merge pull request
    """
    pass