from .._shared import *

app = APIRouter()


@app.get(
    '/repositories/{repository}/refs/{leftRef}/diff/{rightRef}',
    response_model=DiffList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['refs'],
)
def diff_refs(
    repository: str,
    left_ref: str = Path(..., alias='leftRef'),
    right_ref: str = Path(..., alias='rightRef'),
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    prefix: Optional[str] = None,
    delimiter: Optional[str] = None,
    type: Optional[Type4] = ...,
    include_right_stats: Optional[bool] = False,
) -> Union[DiffList, Error]:
    """
    diff references
    """
    pass


@app.get(
    '/repositories/{repository}/refs/{ref}/commits',
    response_model=CommitList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['refs'],
)
def log_commits(
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    objects: Optional[List[str]] = None,
    prefixes: Optional[List[str]] = None,
    limit: Optional[bool] = None,
    first_parent: Optional[bool] = None,
    since: Optional[datetime] = None,
    stop_at: Optional[str] = None,
    repository: str = ...,
    ref: str = ...,
) -> Union[CommitList, Error]:
    """
    get commit log from ref. If both objects and prefixes are empty, return all commits.
    """
    pass


@app.get(
    '/repositories/{repository}/refs/{ref}/objects',
    response_model=bytes,
    responses={
        '206': {'model': bytes},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        '410': {'model': Error},
        '416': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def get_object(
    range: Optional[constr(pattern=r'^bytes=((\d*-\d*,? ?)+)$')] = Header(
        None, alias='Range'
    ),
    if__none__match: Optional[str] = Header(None, alias='If-None-Match'),
    presign: Optional[bool] = None,
    repository: str = ...,
    ref: str = ...,
    path: str = ...,
) -> Union[bytes, Error]:
    """
    get object content
    """
    pass


@app.head(
    '/repositories/{repository}/refs/{ref}/objects',
    response_model=None,
    tags=['objects'],
)
def head_object(
    range: Optional[constr(pattern=r'^bytes=((\d*-\d*,? ?)+)$')] = Header(
        None, alias='Range'
    ),
    repository: str = ...,
    ref: str = ...,
    path: str = ...,
) -> None:
    """
    check if object exists
    """
    pass


@app.get(
    '/repositories/{repository}/refs/{ref}/objects/ls',
    response_model=ObjectStatsList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def list_objects(
    repository: str,
    ref: str = ...,
    user_metadata: Optional[bool] = True,
    presign: Optional[bool] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    delimiter: Optional[str] = None,
    prefix: Optional[str] = None,
) -> Union[ObjectStatsList, Error]:
    """
    list objects under a given prefix
    """
    pass


@app.get(
    '/repositories/{repository}/refs/{ref}/objects/stat',
    response_model=ObjectStats,
    responses={
        '401': {'model': Error},
        '404': {'model': Error},
        '400': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def stat_object(
    repository: str,
    ref: str = ...,
    path: str = ...,
    user_metadata: Optional[bool] = True,
    presign: Optional[bool] = None,
) -> Union[ObjectStats, Error]:
    """
    get object metadata
    """
    pass


@app.get(
    '/repositories/{repository}/refs/{ref}/objects/underlyingProperties',
    response_model=UnderlyingObjectProperties,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['objects'],
)
def get_underlying_properties(
    repository: str, ref: str = ..., path: str = ...
) -> Union[UnderlyingObjectProperties, Error]:
    """
    get object properties on underlying storage
    """
    pass


@app.post(
    '/repositories/{repository}/refs/{sourceRef}/merge/{destinationBranch}',
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
    tags=['refs'],
)
def merge_into_branch(
    repository: str,
    source_ref: str = Path(..., alias='sourceRef'),
    destination_branch: str = Path(..., alias='destinationBranch'),
    body: Merge = None,
) -> Union[MergeResult, Error]:
    """
    merge references
    """
    pass


@app.get(
    '/repositories/{repository}/refs/{sourceRef}/merge/{destinationBranch}',
    response_model=FindMergeBaseResult,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['refs'],
)
def find_merge_base(
    repository: str,
    source_ref: str = Path(..., alias='sourceRef'),
    destination_branch: str = Path(..., alias='destinationBranch'),
) -> Union[FindMergeBaseResult, Error]:
    """
    find the merge base for 2 references
    """
    pass