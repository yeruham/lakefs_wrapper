from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Error(BaseModel):
    message: str = Field(..., description='short message explaining the error')


class ObjectError(BaseModel):
    status_code: int = Field(
        ..., description='HTTP status code associated for operation on path'
    )
    message: str = Field(..., description='short message explaining status_code')
    path: Optional[str] = Field(None, description='affected path')


class ObjectErrorList(BaseModel):
    errors: List[ObjectError]


class ErrorNoACL(BaseModel):
    message: str = Field(..., description='short message explaining the error')
    no_acl: Optional[bool] = Field(
        None, description='true if the group exists but has no ACL'
    )
