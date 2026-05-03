from __future__ import annotations

from pydantic import BaseModel, Field, conint


class Pagination(BaseModel):
    has_more: bool = Field(..., description='Next page is available')
    next_offset: str = Field(..., description='Token used to retrieve the next page')
    results: conint(ge=0) = Field(
        ..., description='Number of values found in the results'
    )
    max_per_page: conint(ge=0) = Field(
        ..., description='Maximal number of entries per page'
    )
