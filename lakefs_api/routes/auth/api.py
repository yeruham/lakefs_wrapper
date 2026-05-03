from .._shared import *

from .auth import app as auth_router
from .users import app as users_router
from .groups import app as groups_router
from .policies import app as policies_router
from .external import app as external_router
from .experimental import app as experimental_router


app = APIRouter()

routers = [
    auth_router,
    users_router,
    groups_router,
    policies_router,
    external_router,
    experimental_router
   ]

for router in routers:
    app.include_router(router)