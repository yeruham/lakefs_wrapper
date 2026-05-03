from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .base import Pagination
from typing import List


class PullRequestStatus(Enum):
    open = 'open'
    closed = 'closed'
    merged = 'merged'


class PullRequestBasic(BaseModel):
    status: Optional[PullRequestStatus] = None
    title: Optional[str] = None
    description: Optional[str] = None


class PullRequest(PullRequestBasic):
    id: str
    creation_date: datetime
    author: str
    source_branch: str
    destination_branch: str
    merged_commit_id: Optional[str] = Field(
        None, description='the commit id of merged PRs'
    )
    closed_date: Optional[datetime] = None


class PullRequestsList(BaseModel):
    pagination: Pagination
    results: List[PullRequest]


class PullRequestCreation(BaseModel):
    title: str
    description: Optional[str] = None
    source_branch: str
    destination_branch: str


class PullRequestCreationResponse(BaseModel):
    id: str = Field(..., description='ID of the pull request')
