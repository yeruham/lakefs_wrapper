from .._shared import *

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
def list_repositories(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    search: Optional[str] = None,
) -> Union[RepositoryList, Error]:
    """
    list repositories
    """
    pass


@app.post(
    '/repositories',
    response_model=None,
    responses={
        '201': {'model': Repository},
        '400': {'model': Error},
        '401': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def create_repository(
    bare: Optional[bool] = False, body: RepositoryCreation = ...
) -> Union[None, Repository, Error]:
    """
    create repository
    """
    pass


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
def get_repository(repository: str) -> Union[Repository, Error]:
    """
    get repository
    """
    pass


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
    """
    delete repository
    """
    pass


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
def get_repository_metadata(repository: str) -> Union[RepositoryMetadata, Error]:
    """
    get repository metadata
    """
    pass


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
    """
    set repository metadata
    """
    pass


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
    """
    delete repository metadata
    """
    pass
