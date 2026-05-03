from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union

from fastapi import APIRouter, Header, Path, Query, HTTPException
from pydantic import conint, constr

from ..models import *  # noqa: F401,F403
from ._routing import NotImplementedRoute