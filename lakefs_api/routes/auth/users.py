from .._shared import *

from ...core.security import get_current_user as core_get_current_user
from ...services.auth import users as users_service

app = APIRouter()


@app.get('/user', response_model=CurrentUser, tags=['auth'])
async def get_current_user(current_user: dict = Depends(core_get_current_user)) -> CurrentUser:
    return await users_service.get_current_user(current_user)


@app.get(
    '/auth/users',
    response_model=UserList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_users(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
) -> Union[UserList, Error]:
    return await users_service.list_users(prefix=prefix, after=after, amount=amount)


@app.post(
    '/auth/users',
    response_model=None,
    responses={
        '201': {'model': User},
        '400': {'model': Error},
        '401': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def create_user(body: UserCreation = None) -> Union[None, User, Error]:
    return await users_service.create_user(body)


@app.get(
    '/auth/users/{userId}',
    response_model=User,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def get_user(user_id: str = Path(..., alias='userId')) -> Union[User, Error]:
    return await users_service.get_user(user_id)


@app.delete(
    '/auth/users/{userId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def delete_user(user_id: str = Path(..., alias='userId')) -> Union[None, Error]:
    # return await users_service.delete_user(user_id)
    raise NotImplementedError

@app.get(
    '/auth/users/{userId}/credentials',
    response_model=CredentialsList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_user_credentials(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    user_id: str = Path(..., alias='userId'),
) -> Union[CredentialsList, Error]:
    return await users_service.list_user_credentials(
        user_id=user_id,
        prefix=prefix,
        after=after,
        amount=amount,
    )


@app.post(
    '/auth/users/{userId}/credentials',
    response_model=None,
    status_code=201,
    responses={
        '201': {'model': CredentialsWithSecret},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def create_credentials(
    user_id: str = Path(..., alias='userId')
) -> Union[None, CredentialsWithSecret, Error]:
    return await users_service.create_credentials(user_id=user_id)


@app.delete(
    '/auth/users/{userId}/credentials/{accessKeyId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def delete_credentials(
    user_id: str = Path(..., alias='userId'),
    access_key_id: str = Path(..., alias='accessKeyId'),
) -> Union[None, Error]:
    # return await users_service.delete_credentials(user_id=user_id, access_key_id=access_key_id)
    raise NotImplementedError

@app.get(
    '/auth/users/{userId}/credentials/{accessKeyId}',
    response_model=Credentials,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def get_credentials(
    user_id: str = Path(..., alias='userId'),
    access_key_id: str = Path(..., alias='accessKeyId'),
) -> Union[Credentials, Error]:
    return await users_service.get_credentials(user_id=user_id, access_key_id=access_key_id)


@app.get(
    '/auth/users/{userId}/groups',
    response_model=GroupList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_user_groups(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    user_id: str = Path(..., alias='userId'),
) -> Union[GroupList, Error]:
    return await users_service.list_user_groups(
        user_id=user_id,
        prefix=prefix,
        after=after,
        amount=amount,
    )


@app.get(
    '/auth/users/{userId}/policies',
    response_model=PolicyList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def list_user_policies(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    effective: Optional[bool] = False,
    user_id: str = Path(..., alias='userId'),
) -> Union[PolicyList, Error]:
    # return await users_service.list_user_policies(
    #     user_id=user_id,
    #     prefix=prefix,
    #     after=after,
    #     amount=amount,
    #     effective=effective,
    # )
    raise NotImplementedError


@app.put(
    '/auth/users/{userId}/policies/{policyId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def attach_policy_to_user(
    user_id: str = Path(..., alias='userId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    # return await users_service.attach_policy_to_user(user_id=user_id, policy_id=policy_id)
    raise NotImplementedError

@app.delete(
    '/auth/users/{userId}/policies/{policyId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
async def detach_policy_from_user(
    user_id: str = Path(..., alias='userId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    # return await users_service.detach_policy_from_user(user_id=user_id, policy_id=policy_id)
    raise NotImplementedError