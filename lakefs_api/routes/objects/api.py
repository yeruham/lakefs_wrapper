from .._shared import *

from objects import app as objects_router
from .staging import app as staging_router
from .experimental import app as experimental_router
from .internal import app as internal_router


app = APIRouter()

routers = [
    objects_router,
    staging_router,
    experimental_router
   ]

for router in routers:
    app.include_router(router)