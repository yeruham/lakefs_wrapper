from .._shared import *

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
def list_policies(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
) -> Union[PolicyList, Error]:
    """
    list policies
    """
    pass


@app.post(
    '/auth/policies',
    response_model=None,
    responses={
        '201': {'model': Policy},
        '400': {'model': Error},
        '401': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
def create_policy(body: Policy) -> Union[None, Policy, Error]:
    """
    create policy
    """
    pass


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
def get_policy(policy_id: str = Path(..., alias='policyId')) -> Union[Policy, Error]:
    """
    get policy
    """
    pass


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
def update_policy(
    policy_id: str = Path(..., alias='policyId'), body: Policy = ...
) -> Union[Policy, Error]:
    """
    update policy
    """
    pass


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
def delete_policy(policy_id: str = Path(..., alias='policyId')) -> Union[None, Error]:
    """
    delete policy
    """
    pass