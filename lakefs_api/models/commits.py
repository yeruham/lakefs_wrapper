from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, RootModel, conint

from .base import Pagination


class Ref(BaseModel):
    id: str
    commit_id: str


class RefList(BaseModel):
    pagination: Pagination
    results: List[Ref]


class RefsDump(BaseModel):
    commits_meta_range_id: str
    tags_meta_range_id: str
    branches_meta_range_id: str


class RefsRestore(BaseModel):
    commits_meta_range_id: str
    tags_meta_range_id: str
    branches_meta_range_id: str
    force: Optional[bool] = False


class CommitOverrides(BaseModel):
    message: Optional[str] = Field(None, description='replace the commit message')
    metadata: Optional[Dict[str, str]] = Field(
        None, description='replace the metadata of the commit'
    )


class Commit(BaseModel):
    id: str
    parents: List[str]
    committer: str
    message: str
    creation_date: int = Field(..., description='Unix Epoch in seconds')
    meta_range_id: str
    metadata: Optional[Dict[str, str]] = None
    generation: Optional[int] = None
    version: Optional[conint(ge=0, le=1)] = None


class CommitList(BaseModel):
    pagination: Pagination
    results: List[Commit]


class CommitCreation(BaseModel):
    message: str
    metadata: Optional[Dict[str, str]] = None
    date: Optional[int] = Field(
        None,
        description='set date to override creation date in the commit (Unix Epoch in seconds)',
    )
    allow_empty: Optional[bool] = Field(
        False, description='sets whether a commit can contain no changes'
    )
    force: Optional[bool] = False


class CommitRecordCreation(BaseModel):
    commit_id: str = Field(..., description='id of the commit record')
    version: conint(ge=0, le=1) = Field(..., description='version of the commit record')
    committer: str = Field(..., description='committer of the commit record')
    message: str = Field(..., description='message of the commit record')
    metarange_id: str = Field(..., description='metarange_id of the commit record')
    creation_date: int = Field(..., description='Unix Epoch in seconds')
    parents: List[str] = Field(..., description='parents of the commit record')
    metadata: Optional[Dict[str, str]] = Field(
        None, description='metadata of the commit record'
    )
    generation: int = Field(..., description='generation of the commit record')
    force: Optional[bool] = False


class FindMergeBaseResult(BaseModel):
    source_commit_id: str = Field(..., description='The commit ID of the merge source')
    destination_commit_id: str = Field(
        ..., description='The commit ID of the merge destination'
    )
    base_commit_id: str = Field(..., description='The commit ID of the merge base')


class MergeResult(BaseModel):
    reference: str


class Merge(BaseModel):
    message: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    strategy: Optional[str] = Field(
        None,
        description=(
            "In case of a merge conflict, this option will force the merge process to "
            "automatically favor changes from the dest branch ('dest-wins') or from the "
            "source branch('source-wins'). In case no selection is made, the merge process "
            "will fail in case of a conflict"
        ),
    )
    force: Optional[bool] = Field(
        False,
        description='Allow merge into a read-only branch or into a branch with the same content',
    )
    allow_empty: Optional[bool] = Field(
        False, description='Allow merge when the branches have the same content'
    )
    squash_merge: Optional[bool] = Field(
        False,
        description=(
            "If set, set only the destination branch as a parent, which \"squashes\" the merge to\n"
            "appear as a single commit on the destination branch."
        ),
    )


class BranchCreation(BaseModel):
    name: str
    source: str
    force: Optional[bool] = False
    hidden: Optional[bool] = Field(
        False,
        description='When set, branch will not show up when listing branches by default. *EXPERIMENTAL*',
    )


class TagCreation(BaseModel):
    id: str = Field(..., description='ID of tag to create')
    ref: str = Field(..., description='the commit to tag')
    force: Optional[bool] = False


class ResetCreation(BaseModel):
    type: str = Field(..., description='What to reset according to path.')
    path: Optional[str] = None
    force: Optional[bool] = False


class RevertCreation(BaseModel):
    ref: str = Field(..., description='the commit to revert, given by a ref')
    commit_overrides: Optional[CommitOverrides] = None
    parent_number: int = Field(
        ...,
        description='when reverting a merge commit, the parent number (starting from 1) relative to which to perform the revert.',
    )
    force: Optional[bool] = False
    allow_empty: Optional[bool] = Field(
        False, description='allow empty commit (revert without changes)'
    )


class CherryPickCreation(BaseModel):
    ref: str = Field(..., description='the commit to cherry-pick, given by a ref')
    parent_number: Optional[int] = Field(
        None,
        description='When cherry-picking a merge commit, the parent number (starting from 1) with which to perform the diff.\nThe default branch is parent 1.\n',
    )
    commit_overrides: Optional[CommitOverrides] = None
    force: Optional[bool] = False
