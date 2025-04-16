from typing import TypedDict, List, Dict, Any


class SearchResultDict(TypedDict):
    """Search result containing results and total count."""

    results: List[Dict[str, Any]]
    total: int
