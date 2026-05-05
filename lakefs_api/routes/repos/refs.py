from .._shared import *
from lakefs_api.core.lakefs_client import _client

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
async def diff_refs(
    repository: str,
    left_ref: str = Path(..., alias='leftRef'),
    right_ref: str = Path(..., alias='rightRef'),
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    prefix: Optional[str] = None,
    delimiter: Optional[str] = None,
    type: Optional[Type4] = ...,
    include_right_stats: Optional[bool] = False,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[DiffList, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.refs_api.diff_refs(repository=repository, left_ref=left_ref, right_ref=right_ref, prefix=prefix, after=after, amount=amount, delimiter=delimiter, type=type, include_right_stats=include_right_stats)


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
async def log_commits(
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
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[CommitList, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.refs_api.log_commits(repository=repository, ref=ref, after=after, amount=amount, objects=objects, prefixes=prefixes, limit=limit, first_parent=first_parent, since=since, stop_at=stop_at)


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
    raise NotImplementedError


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
async def merge_into_branch(
    repository: str,
    source_ref: str = Path(..., alias='sourceRef'),
    destination_branch: str = Path(..., alias='destinationBranch'),
    body: Merge = None,
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[MergeResult, Error]:
    await require_permission(current_user.username, LakeFSAction.write, repository)
    return _client.refs_api.merge_into_branch(repository=repository, source_ref=source_ref, destination_branch=destination_branch, merge=body)


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
async def find_merge_base(
    repository: str,
    source_ref: str = Path(..., alias='sourceRef'),
    destination_branch: str = Path(..., alias='destinationBranch'),
    current_user: BasicUser = Depends(core_get_current_user),
) -> Union[FindMergeBaseResult, Error]:
    await require_permission(current_user.username, LakeFSAction.read, repository)
    return _client.refs_api.find_merge_base(repository=repository, source_ref=source_ref, destination_branch=destination_branch)