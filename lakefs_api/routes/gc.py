from fastapi import APIRouter

app = APIRouter()


@app.post(
    '/repositories/{repository}/gc/prepare_commits',
    response_model=None,
    responses={
        '201': {'model': GarbageCollectionPrepareResponse},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def prepare_garbage_collection_commits(
    repository: str,
) -> Union[None, GarbageCollectionPrepareResponse, Error]:
    """
    save lists of active commits for garbage collection
    """
    pass


@app.post(
    '/repositories/{repository}/gc/prepare_commits/async',
    response_model=None,
    responses={
        '202': {'model': TaskCreation},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def prepare_garbage_collection_commits_async(
    repository: str,
) -> Union[None, TaskCreation, Error]:
    """
    prepare gc commits
    """
    pass


@app.get(
    '/repositories/{repository}/gc/prepare_commits/status',
    response_model=PrepareGarbageCollectionCommitsStatus,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def prepare_garbage_collection_commits_status(
    id: str, repository: str = ...
) -> Union[PrepareGarbageCollectionCommitsStatus, Error]:
    """
    get status of prepare gc commits operation
    """
    pass


@app.post(
    '/repositories/{repository}/gc/prepare_uncommited',
    response_model=None,
    responses={
        '201': {'model': PrepareGCUncommittedResponse},
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def prepare_garbage_collection_uncommitted(
    repository: str, body: PrepareGCUncommittedRequest = None
) -> Union[None, PrepareGCUncommittedResponse, Error]:
    """
    save repository uncommitted metadata for garbage collection
    """
    pass


@app.get(
    '/repositories/{repository}/gc/rules',
    response_model=GarbageCollectionRules,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def internal_get_garbage_collection_rules(
    repository: str,
) -> Union[GarbageCollectionRules, Error]:
    pass


@app.post(
    '/repositories/{repository}/gc/rules',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def internal_set_garbage_collection_rules(
    repository: str, body: GarbageCollectionRules = ...
) -> Union[None, Error]:
    pass


@app.delete(
    '/repositories/{repository}/gc/rules',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def internal_delete_garbage_collection_rules(repository: str) -> Union[None, Error]:
    pass


@app.get(
    '/repositories/{repository}/gc/rules/set_allowed',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def set_garbage_collection_rules_preflight(repository: str) -> Union[None, Error]:
    pass


@app.get(
    '/repositories/{repository}/settings/gc_rules',
    response_model=GarbageCollectionRules,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def get_g_c_rules(repository: str) -> Union[GarbageCollectionRules, Error]:
    """
    get repository GC rules
    """
    pass


@app.put(
    '/repositories/{repository}/settings/gc_rules',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def set_g_c_rules(
    repository: str, body: GarbageCollectionRules = ...
) -> Union[None, Error]:
    pass


@app.delete(
    '/repositories/{repository}/settings/gc_rules',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def delete_g_c_rules(repository: str) -> Union[None, Error]:
    pass