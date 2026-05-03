from .._shared import *

app = APIRouter()


@app.post(
    '/repositories/{repository}/restore',
    response_model=None,
    responses={
        '202': {'model': TaskInfo},
        '400': {'model': Error},
        '403': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def restore_submit(
    repository: str, body: RefsRestore = ...
) -> Union[None, TaskInfo, Error]:
    """
    Restore repository from a dump in the object store
    """
    pass


@app.get(
    '/repositories/{repository}/restore',
    response_model=RepositoryRestoreStatus,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def restore_status(
    task_id: str, repository: str = ...
) -> Union[RepositoryRestoreStatus, Error]:
    """
    Status of a restore request
    """
    pass