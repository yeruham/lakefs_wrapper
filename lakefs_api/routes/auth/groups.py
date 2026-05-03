from fastapi import APIRouter

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
def list_groups(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
) -> Union[GroupList, Error]:
    """
    list groups
    """
    pass


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
def create_group(body: GroupCreation = None) -> Union[None, Group, Error]:
    """
    create group
    """
    pass


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
def get_group(group_id: str = Path(..., alias='groupId')) -> Union[Group, Error]:
    """
    get group
    """
    pass


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
def delete_group(group_id: str = Path(..., alias='groupId')) -> Union[None, Error]:
    """
    delete group
    """
    pass






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
def set_group_a_c_l(
    group_id: str = Path(..., alias='groupId'), body: ACL = ...
) -> Union[None, Error]:
    """
    set ACL of group
    """
    pass


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
def get_group_a_c_l(
    group_id: str = Path(..., alias='groupId')
) -> Union[ACL, Error, ErrorNoACL]:
    """
    get ACL of group
    """
    pass


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
def list_group_members(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    group_id: str = Path(..., alias='groupId'),
) -> Union[UserList, Error]:
    """
    list group members
    """
    pass


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
def add_group_membership(
    group_id: str = Path(..., alias='groupId'), user_id: str = Path(..., alias='userId')
) -> Union[None, Error]:
    """
    add group membership
    """
    pass


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
def delete_group_membership(
    group_id: str = Path(..., alias='groupId'), user_id: str = Path(..., alias='userId')
) -> Union[None, Error]:
    """
    delete group membership
    """
    pass


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
def list_group_policies(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    group_id: str = Path(..., alias='groupId'),
) -> Union[PolicyList, Error]:
    """
    list group policies
    """
    pass


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
def attach_policy_to_group(
    group_id: str = Path(..., alias='groupId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    """
    attach policy to group
    """
    pass


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
def detach_policy_from_group(
    group_id: str = Path(..., alias='groupId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    """
    detach policy from group
    """
    pass