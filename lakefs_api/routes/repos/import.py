from fastapi import APIRouter

app = APIRouter()


@app.get(
    '/repositories/{repository}/branches/{branch}/import',
    response_model=ImportStatus,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['import'],
)
def import_status(
    id: str, repository: str = ..., branch: str = ...
) -> Union[ImportStatus, Error]:
    """
    get import status
    """
    pass


@app.post(
    '/repositories/{repository}/branches/{branch}/import',
    response_model=None,
    responses={
        '202': {'model': ImportCreationResponse},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['import'],
)
def import_start(
    repository: str, branch: str = ..., body: ImportCreation = ...
) -> Union[None, ImportCreationResponse, Error]:
    """
    import data from object store
    """
    pass


@app.delete(
    '/repositories/{repository}/branches/{branch}/import',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['import'],
)
def import_cancel(
    id: str, repository: str = ..., branch: str = ...
) -> Union[None, Error]:
    """
    cancel ongoing import
    """
    pass