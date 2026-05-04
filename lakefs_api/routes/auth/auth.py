from .._shared import *
from ...services.auth import auth as auth_service

app = APIRouter()


@app.get(
    '/auth/capabilities',
    response_model=AuthCapabilities,
    responses={'default': {'model': Error}},
    tags=['internal'],
)
async def get_auth_capabilities() -> Union[AuthCapabilities, Error]:
    """
    list authentication capabilities supported
    """
    return await auth_service.get_auth_capabilities()


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
async def login(body: LoginInformation = None) -> Union[AuthenticationToken, Error]:
    """
    perform a login
    """
    return await auth_service.login(body)


@app.get(
    '/oidc/callback',
    response_model=None,
    responses={'default': {'model': Error}},
    tags=['auth'],
)
async def oauth_callback() -> Union[None, Error]:
    raise NotImplementedError