from typing import TypedDict, List, Dict, Any


class CustomFieldDict(TypedDict):
    """Custom field definition."""

    uuid: str
    name: str
    type: str
    multiple: bool
    options: List[Dict[str, Any]]
    associations: List[str]
