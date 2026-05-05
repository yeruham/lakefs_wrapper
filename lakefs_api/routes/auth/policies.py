from .._shared import *

from ...services.auth import policies as policies_service

app = APIRouter()


@app.get(
    '/auth/policies',
    response_model=PolicyList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_policies(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
) -> Union[PolicyList, Error]:
    return await policies_service.list_policies(prefix=prefix, after=after, amount=amount)


@app.post(
    '/auth/policies',
    response_model=None,
    status_code=201,
    responses={
        '201': {'model': Policy},
        '400': {'model': Error},
        '401': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def create_policy(body: Policy) -> Union[None, Policy, Error]:
    return await policies_service.create_policy(body=body)


@app.get(
    '/auth/policies/{policyId}',
    response_model=Policy,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def get_policy(policy_id: str = Path(..., alias='policyId')) -> Union[Policy, Error]:
    return await policies_service.get_policy(policy_id=policy_id)


@app.put(
    '/auth/policies/{policyId}',
    response_model=Policy,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def update_policy(
    policy_id: str = Path(..., alias='policyId'), body: Policy = ...
) -> Union[Policy, Error]:
    return await policies_service.update_policy(policy_id=policy_id, body=body)


@app.delete(
    '/auth/policies/{policyId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def delete_policy(policy_id: str = Path(..., alias='policyId')) -> Union[None, Error]:
    return await policies_service.delete_policy(policy_id=policy_id)