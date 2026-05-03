from fastapi import HTTPException, status
from ..services.auth.group_service import user_can

# ── Permission helper (reuse same pattern) ────────────────────────────────────

def _is_admin(current_user: dict) -> bool:
    return "admins" in current_user.get("groups", [])


async def _require_permission(db, user: dict, repo: str, action: str):
    if _is_admin(user):
        return
    allowed = await user_can(db, user["groups"], repo, action)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Your groups do not have '{action}' on repo '{repo}'",
        )