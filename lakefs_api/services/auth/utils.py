from datetime import datetime, timezone
from typing import Any, Optional


def _now_ts() -> int:
    return int(datetime.now(timezone.utc).timestamp())



def _paginate(items: list[Any], item_cursor: str, after: Optional[str], amount: Optional[int]) -> tuple[list[Any], bool, str]:
    if amount is None or amount < 0:
        amount = len(items)
    start = 0
    if after:
        for idx, item in enumerate(items):
            if getattr(item, item_cursor, "") > after:
                start = idx
                break
        else:
            start = len(items)
    sliced = items[start : start + amount]
    has_more = start + amount < len(items)
    next_offset = getattr(sliced[-1], item_cursor, "") if has_more and sliced else ""
    return sliced, has_more, next_offset