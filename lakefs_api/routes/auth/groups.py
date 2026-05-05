from .._shared import *

from ...services.auth import groups as groups_service

app = APIRouter()


@app.get(
    '/auth/groups',
    response_model=GroupList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_groups(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
) -> Union[GroupList, Error]:
    return await groups_service.list_groups(prefix=prefix, after=after, amount=amount)


@app.post(
    '/auth/groups',
    response_model=None,
    responses={
        '201': {'model': Group},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def create_group(body: GroupCreation = None) -> Union[None, Group, Error]:
    return await groups_service.create_group(body)


@app.get(
    '/auth/groups/{groupId}',
    response_model=Group,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def get_group(group_id: str = Path(..., alias='groupId')) -> Union[Group, Error]:
    return await groups_service.get_group(group_id)


@app.delete(
    '/auth/groups/{groupId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def delete_group(group_id: str = Path(..., alias='groupId')) -> Union[None, Error]:
    return await groups_service.delete_group(group_id)


@app.post(
    '/auth/groups/{groupId}/acl',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def set_group_a_c_l(
    group_id: str = Path(..., alias='groupId'), body: ACL = ...
) -> Union[None, Error]:
    return await groups_service.set_group_acl(group_id=group_id, body=body)


@app.get(
    '/auth/groups/{groupId}/acl',
    response_model=ACL,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': ErrorNoACL},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def get_group_a_c_l(
    group_id: str = Path(..., alias='groupId')
) -> Union[ACL, Error, ErrorNoACL]:
    return await groups_service.get_group_acl(group_id=group_id)


@app.get(
    '/auth/groups/{groupId}/members',
    response_model=UserList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_group_members(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    group_id: str = Path(..., alias='groupId'),
) -> Union[UserList, Error]:
    return await groups_service.list_group_members(
        group_id=group_id,
        prefix=prefix,
        after=after,
        amount=amount,
    )


@app.put(
    '/auth/groups/{groupId}/members/{userId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def add_group_membership(
    group_id: str = Path(..., alias='groupId'), user_id: str = Path(..., alias='userId')
) -> Union[None, Error]:
    return await groups_service.add_group_membership(group_id=group_id, user_id=user_id)


@app.delete(
    '/auth/groups/{groupId}/members/{userId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def delete_group_membership(
    group_id: str = Path(..., alias='groupId'), user_id: str = Path(..., alias='userId')
) -> Union[None, Error]:
    return await groups_service.delete_group_membership(group_id=group_id, user_id=user_id)


@app.get(
    '/auth/groups/{groupId}/policies',
    response_model=PolicyList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_group_policies(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    group_id: str = Path(..., alias='groupId'),
) -> Union[PolicyList, Error]:
    return await groups_service.list_group_policies(
        group_id=group_id,
        prefix=prefix,
        after=after,
        amount=amount,
    )


@app.put(
    '/auth/groups/{groupId}/policies/{policyId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def attach_policy_to_group(
    group_id: str = Path(..., alias='groupId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    return await groups_service.attach_policy_to_group(group_id=group_id, policy_id=policy_id)


@app.delete(
    '/auth/groups/{groupId}/policies/{policyId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def detach_policy_from_group(
    group_id: str = Path(..., alias='groupId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    return await groups_service.detach_policy_from_group(group_id=group_id, policy_id=policy_id)