from .._shared import *

app = APIRouter()


@app.put(
    '/repositories/{repository}/branches/{branch}/objects',
    response_model=None,
    responses={
        '201': {'model': ObjectStats},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def stage_object(
    repository: str, branch: str = ..., path: str = ..., body: ObjectStageCreation = ...
) -> Union[None, ObjectStats, Error]:
    """
    stage an object's metadata for the given branch
    """
    pass


@app.get(
    '/repositories/{repository}/branches/{branch}/objects/stage_allowed',
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
def upload_object_preflight(
    repository: str, branch: str = ..., path: str = ...
) -> Union[None, Error]:
    pass
