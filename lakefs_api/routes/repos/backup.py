from fastapi import APIRouter

app = APIRouter()


@app.post(
    '/repositories/{repository}/dump',
    response_model=None,
    responses={
        '202': {'model': TaskInfo},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def dump_submit(repository: str) -> Union[None, TaskInfo, Error]:
    """
    Backup the repository metadata (tags, commits, branches) and save the backup to the object store.
    """
    pass


@app.get(
    '/repositories/{repository}/dump',
    response_model=RepositoryDumpStatus,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def dump_status(
    task_id: str, repository: str = ...
) -> Union[RepositoryDumpStatus, Error]:
    """
    Status of a repository dump task
    """
    pass


@app.put(
    '/repositories/{repository}/refs/dump',
    response_model=None,
    responses={
        '201': {'model': RefsDump},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def dump_refs(repository: str) -> Union[None, RefsDump, Error]:
    """
        Dump repository refs (tags, commits, branches) to object store
    Deprecated: a new API will introduce long running operations

    """
    pass




@app.put(
    '/repositories/{repository}/refs/restore',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def restore_refs(repository: str, body: RefsRestore = ...) -> Union[None, Error]:
    """
        Restore repository refs (tags, commits, branches) from object store.
    Deprecated: a new API will introduce long running operations

    """
    pass