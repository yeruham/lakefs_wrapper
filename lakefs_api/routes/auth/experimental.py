from fastapi import APIRouter

app = APIRouter()


@app.post(
    '/sts/login',
    response_model=AuthenticationToken,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        'default': {'model': Error},
    },
    tags=['experimental'],
)
def sts_login(body: StsAuthRequest) -> Union[AuthenticationToken, Error]:
    """
    perform a login with STS
    """
    pass