from .._shared import *

app = APIRouter()


@app.post(
    '/repositories/{repository}/refs/{branch}/symlink',
    response_model=None,
    responses={
        '201': {'model': StorageURI},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def create_symlink_file(
    repository: str, branch: str = ..., location: Optional[str] = None
) -> Union[None, StorageURI, Error]:
    """
    creates symlink files corresponding to the given directory
    """
    pass


@app.post(
    '/statistics',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def post_stats_events(body: StatsEventsList) -> Union[None, Error]:
    """
    post stats events, this endpoint is meant for internal use only
    """
    pass
