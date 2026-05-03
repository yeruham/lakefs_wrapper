from ._shared import *

app = APIRouter()


@app.post(
    '/setup_lakefs',
    response_model=CredentialsWithSecret,
    responses={
        '400': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def setup(body: Setup) -> Union[CredentialsWithSecret, Error]:
    """
    setup lakeFS and create a first user
    """
    pass


@app.get(
    '/setup_lakefs',
    response_model=SetupState,
    responses={'default': {'model': Error}},
    tags=['internal'],
)
def get_setup_state() -> Union[SetupState, Error]:
    """
    check if the lakeFS installation is already set up
    """
    pass


@app.post(
    '/setup_comm_prefs',
    response_model=None,
    responses={
        '400': {'model': Error},
        '409': {'model': Error},
        '412': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def setup_comm_prefs(body: CommPrefsInput) -> Union[None, Error]:
    """
    setup communications preferences
    """
    pass