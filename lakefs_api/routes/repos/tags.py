from .._shared import *

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
def list_tags(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    repository: str = ...,
) -> Union[RefList, Error]:
    """
    list tags
    """
    pass


@app.post(
    '/repositories/{repository}/tags',
    response_model=None,
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
def create_tag(repository: str, body: TagCreation = ...) -> Union[None, Ref, Error]:
    """
    create tag
    """
    pass


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
def get_tag(repository: str, tag: str = ...) -> Union[Ref, Error]:
    """
    get tag
    """
    pass


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
def delete_tag(
    force: Optional[bool] = None, repository: str = ..., tag: str = ...
) -> Union[None, Error]:
    """
    delete tag
    """
    pass