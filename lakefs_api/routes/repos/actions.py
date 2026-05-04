from .._shared import *

app = APIRouter()



@app.get(
    '/repositories/{repository}/actions/runs',
    response_model=ActionRunList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['actions'],
)
def list_repository_runs(
    repository: str,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    branch: Optional[str] = None,
    commit: Optional[str] = None,
) -> Union[ActionRunList, Error]:
    """
    list runs
    """
    pass


@app.get(
    '/repositories/{repository}/actions/runs/{run_id}',
    response_model=ActionRun,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['actions'],
)
def get_run(repository: str, run_id: str = ...) -> Union[ActionRun, Error]:
    """
    get a run
    """
    pass


@app.get(
    '/repositories/{repository}/actions/runs/{run_id}/hooks',
    response_model=HookRunList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['actions'],
)
def list_run_hooks(
    repository: str,
    run_id: str = ...,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
) -> Union[HookRunList, Error]:
    """
    list run hooks
    """
    pass


@app.get(
    '/repositories/{repository}/actions/runs/{run_id}/hooks/{hook_run_id}/output',
    response_model=bytes,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['actions'],
)
def get_run_hook_output(
    repository: str, run_id: str = ..., hook_run_id: str = ...
) -> Union[bytes, Error]:
    """
    get run hook output
    """
    pass