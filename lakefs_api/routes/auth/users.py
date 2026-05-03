from fastapi import APIRouter

app = APIRouter()


@app.get('/user', response_model=CurrentUser, tags=['auth'])
def get_current_user() -> CurrentUser:
    """
    get current user
    """
    pass


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
def list_users(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
) -> Union[UserList, Error]:
    """
    list users
    """
    pass


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
def create_user(body: UserCreation = None) -> Union[None, User, Error]:
    """
    create user
    """
    pass


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
def get_user(user_id: str = Path(..., alias='userId')) -> Union[User, Error]:
    """
    get user
    """
    pass


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
def delete_user(user_id: str = Path(..., alias='userId')) -> Union[None, Error]:
    """
    delete user
    """
    pass




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
def list_user_credentials(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    user_id: str = Path(..., alias='userId'),
) -> Union[CredentialsList, Error]:
    """
    list user credentials
    """
    pass


@app.post(
    '/auth/users/{userId}/credentials',
    response_model=None,
    responses={
        '201': {'model': CredentialsWithSecret},
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
def create_credentials(
    user_id: str = Path(..., alias='userId')
) -> Union[None, CredentialsWithSecret, Error]:
    """
    create credentials
    """
    pass



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
def delete_credentials(
    user_id: str = Path(..., alias='userId'),
    access_key_id: str = Path(..., alias='accessKeyId'),
) -> Union[None, Error]:
    """
    delete credentials
    """
    pass



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
def get_credentials(
    user_id: str = Path(..., alias='userId'),
    access_key_id: str = Path(..., alias='accessKeyId'),
) -> Union[Credentials, Error]:
    """
    get credentials
    """
    pass


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
def list_user_groups(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    user_id: str = Path(..., alias='userId'),
) -> Union[GroupList, Error]:
    """
    list user groups
    """
    pass


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
def list_user_policies(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    effective: Optional[bool] = False,
    user_id: str = Path(..., alias='userId'),
) -> Union[PolicyList, Error]:
    """
    list user policies
    """
    pass


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
def attach_policy_to_user(
    user_id: str = Path(..., alias='userId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    """
    attach policy to user
    """
    pass


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
def detach_policy_from_user(
    user_id: str = Path(..., alias='userId'),
    policy_id: str = Path(..., alias='policyId'),
) -> Union[None, Error]:
    """
    detach policy from user
    """
    pass