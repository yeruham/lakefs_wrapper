from .._shared import *

from .repositories  import app as repositories_router
from .branches import app as branches_router
from .commits import app as commits_router
from .refs import app as refs_router
from .tags import app as tags_router
from .protection import app as protection_router
from .actions import app as actions_router
from .objects import app as objects_router
from .restore import app as restore_router
from .imports import app as imports_router
from .metadata import app as metadata_router
from .internal import app as internal_router
from .experimental import app as experimental_router
from .backup import app as backup_router


app = APIRouter()

routers = [
    repositories_router,
    branches_router,
    commits_router,
    refs_router,
    tags_router,
    protection_router,
    actions_router,
    objects_router,
    restore_router,
    imports_router,
    metadata_router,
    backup_router,
    internal_router,
    experimental_router
   ]

for router in routers:
    app.include_router(router)