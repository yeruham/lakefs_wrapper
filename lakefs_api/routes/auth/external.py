from .._shared import *

app = APIRouter()


@app.post(
    '/auth/external/principal/login',
    response_model=AuthenticationToken,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['external', 'experimental', 'auth'],
)
def external_principal_login(
    body: ExternalLoginInformation = None,
) -> Union[AuthenticationToken, Error]:
    """
    perform a login using an external authenticator
    """
    pass


@app.get(
    '/auth/external/principals',
    response_model=ExternalPrincipal,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth', 'external', 'experimental'],
)
def get_external_principal(
    principal_id: str = Query(..., alias='principalId')
) -> Union[ExternalPrincipal, Error]:
    """
    describe external principal by id
    """
    pass


@app.post(
    '/auth/users/{userId}/external/principals',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth', 'external', 'experimental'],
)
def create_user_external_principal(
    user_id: str = Path(..., alias='userId'),
    principal_id: str = Query(..., alias='principalId'),
    body: ExternalPrincipalCreation = None,
) -> Union[None, Error]:
    """
    attach external principal to user
    """
    pass


@app.delete(
    '/auth/users/{userId}/external/principals',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth', 'external', 'experimental'],
)
def delete_user_external_principal(
    user_id: str = Path(..., alias='userId'),
    principal_id: str = Query(..., alias='principalId'),
) -> Union[None, Error]:
    """
    delete external principal from user
    """
    pass


@app.get(
    '/auth/users/{userId}/external/principals/ls',
    response_model=ExternalPrincipalList,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth', 'external', 'experimental'],
)
def list_user_external_principals(
    prefix: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[conint(ge=-1, le=1000)] = 100,
    user_id: str = Path(..., alias='userId'),
) -> Union[ExternalPrincipalList, Error]:
    """
    list user external policies attached to a user
    """
    pass