import lakefs_sdk
from lakefs_sdk.client import LakeFSClient
from lakefs_sdk import models as lm, Commit, Repository
from lakefs_sdk.exceptions import NotFoundException, ServiceException
from fastapi import HTTPException

from ...core.config import get_settings
from ...models import RepositoryList

settings = get_settings()


def _get_client() -> LakeFSClient:
    cfg = lakefs_sdk.Configuration(
        host=settings.lakefs_endpoint,
        username=settings.lakefs_access_key,
        password=settings.lakefs_secret_key,
    )
    return LakeFSClient(configuration=cfg)


def _handle_lakefs_error(e: Exception):
    if isinstance(e, NotFoundException):
        raise HTTPException(status_code=404, detail=str(e.body) if hasattr(e, "body") else "Not found in lakeFS")
    if isinstance(e, ServiceException):
        raise HTTPException(status_code=502, detail=f"lakeFS error: {e.body if hasattr(e, 'body') else str(e)}")
    raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# ── Repositories ──────────────────────────────────────────────────────────────

async def list_repos() -> RepositoryList:
    try:
        c = _get_client()
        resp = c.repositories_api.list_repositories()
        return resp
    except Exception as e:
        _handle_lakefs_error(e)


async def create_repo(repo_id: str, storage_namespace: str, default_branch: str = "main") -> Repository:
    try:
        c = _get_client()
        body = lm.RepositoryCreation(
            name=repo_id,
            storage_namespace=f"s3://{settings.minio_bucket}/{storage_namespace}",
            default_branch=default_branch,
        )
        repo = c.repositories_api.create_repository(body)
        return repo
    except Exception as e:
        _handle_lakefs_error(e)


async def delete_repo(repo_id: str) -> None:
    try:
        c = _get_client()
        c.repositories_api.delete_repository(repo_id)
    except Exception as e:
        _handle_lakefs_error(e)


# ── Branches ──────────────────────────────────────────────────────────────────

async def list_branches(repo_id: str) -> list:
    try:
        c = _get_client()
        resp = c.branches_api.list_branches(repo_id)
        return [b.to_dict() for b in resp.results]
    except Exception as e:
        _handle_lakefs_error(e)


async def create_branch(repo_id: str, branch_name: str, source_branch: str) -> dict:
    try:
        c = _get_client()
        body = lm.BranchCreation(name=branch_name, source=source_branch)
        ref = c.branches_api.create_branch(repo_id, body)
        return {"branch": branch_name, "commit_id": ref}
    except Exception as e:
        _handle_lakefs_error(e)


async def delete_branch(repo_id: str, branch_name: str) -> None:
    try:
        c = _get_client()
        c.branches_api.delete_branch(repo_id, branch_name)
    except Exception as e:
        _handle_lakefs_error(e)


# ── Commits ───────────────────────────────────────────────────────────────────

async def list_commits(repo_id: str, branch: str) -> list:
    try:
        c = _get_client()
        resp = c.commits_api.log_branch_commits(repo_id, branch)
        return [cm.to_dict() for cm in resp.results]
    except Exception as e:
        _handle_lakefs_error(e)


async def commit(repo_id: str, branch: str, message: str, metadata: dict | None = None) -> Commit:
    try:
        c = _get_client()
        body = lm.CommitCreation(message=message, metadata=metadata or {})
        cm = c.commits_api.commit(repo_id, branch, body)
        return cm.to_dict()
    except Exception as e:
        _handle_lakefs_error(e)


# ── Merges ────────────────────────────────────────────────────────────────────

async def merge_branches(repo_id: str, source_branch: str, destination_branch: str, message: str = "") -> dict:
    try:
        c = _get_client()
        body = lm.Merge(message=message)
        result = c.refs_api.merge_into_branch(repo_id, source_branch, destination_branch, merge=body)
        return result.to_dict()
    except Exception as e:
        _handle_lakefs_error(e)


# ── Diff ──────────────────────────────────────────────────────────────────────

async def diff_refs(repo_id: str, left_ref: str, right_ref: str) -> list:
    try:
        c = _get_client()
        resp = c.refs_api.diff_refs(repo_id, left_ref, right_ref)
        return [d.to_dict() for d in resp.results]
    except Exception as e:
        _handle_lakefs_error(e)