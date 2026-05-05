import fnmatch
from ...core.database import get_groups_by_ids, get_user_by_id, get_policies_by_ids
from ...models import Effect, Policy, Statement, User
from .schemas import UserInDB, LakeFSAction


def _resource_matches(pattern: str, repo_id: str) -> bool:
    return pattern == "*" or fnmatch.fnmatch(repo_id, pattern)


def _action_matches(pattern: str, action: LakeFSAction) -> bool:
    return pattern == "*" or fnmatch.fnmatch(action.value, pattern)


def _statement_matches(statement: Statement, action: LakeFSAction, repo_id: str) -> bool:
    return (
        _resource_matches(statement.resource, repo_id)
        and any(_action_matches(a, action) for a in statement.action)
    )


async def _collect_all_policies(user_in_db: UserInDB) -> list[Policy]:
    policy_ids: set[str] = set(user_in_db.policy_ids)

    if user_in_db.groups:
        groups = await get_groups_by_ids( user_in_db.groups)
        for group in groups:
            policy_ids.update(group.get("policy_ids", []))

    return await get_policies_by_ids(list(policy_ids))


async def is_allowed(user: User, action: LakeFSAction, repo_id: str) -> bool:

    user_in_db = await get_user_by_id(user.id)
    if user_in_db is None:
        return False

    policies = await _collect_all_policies(user_in_db)
    all_statements = [stmt for policy in policies for stmt in policy.statement]
    matching = [s for s in all_statements if _statement_matches(s, action, repo_id)]

    if not matching:
        return False  # default deny

    if any(s.effect == Effect.deny for s in matching):
        return False

    return any(s.effect == Effect.allow for s in matching)


async def require_permission(user: User, action: LakeFSAction, repo_id: str) -> None:
    if not await is_allowed(user, action, repo_id):
        raise PermissionError(
            f"User '{user.id}' is not allowed to perform "
            f"'{action.value}' on repo '{repo_id}'"
        )
