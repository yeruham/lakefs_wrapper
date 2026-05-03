from fastapi import APIRouter

app = APIRouter()


@app.get(
    '/auth/capabilities',
    response_model=AuthCapabilities,
    responses={'default': {'model': Error}},
    tags=['internal'],
)
def get_auth_capabilities() -> Union[AuthCapabilities, Error]:
    """
    list authentication capabilities supported
    """
    pass


@app.post(
    '/auth/login',
    response_model=AuthenticationToken,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['auth'],
)
def login(body: LoginInformation = None) -> Union[AuthenticationToken, Error]:
    """
    perform a login
    """
    pass


@app.get(
    '/oidc/callback',
    response_model=None,
    responses={'default': {'model': Error}},
    tags=['auth'],
)
def oauth_callback() -> Union[None, Error]:
    pass
