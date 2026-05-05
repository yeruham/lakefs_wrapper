from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union

from fastapi import APIRouter, Header, Path, Query, HTTPException
from pydantic import conint, constr
from fastapi import Depends

from ..models import *  # noqa: F401,F403
from ..core.security import get_current_user as core_get_current_user, BasicUser
from ..services.auth.permissions import require_permission
from ..services.auth.schemas import LakeFSAction
from ._routing import NotImplementedRoute