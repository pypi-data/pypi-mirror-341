from typing import TypedDict, Optional, Any, List
from .workspace import WorkspaceDict


class TaskUserDict(TypedDict):
    """Task user information."""

    email: str


class TaskCompanyDict(TypedDict):
    """Task company information."""

    uuid: str
    name: str
    color: str


class TaskTeamDict(TypedDict):
    """Task team information."""

    uuid: str
    name: str
    color: str


class TaskProjectDict(TypedDict):
    """Task project information."""

    uuid: str
    name: str
    isFavorite: bool


class TaskDict(TypedDict):
    """Project task information."""

    uuid: str
    description: str
    status: str
    number: int
    estimatedEndDate: Optional[str]
    endDate: Optional[str]
    created: str
    ordering: Optional[int]
    updated: str
    note: Optional[Any]
    project: TaskProjectDict
    user: TaskUserDict
    # assets: Optional[List[TaskAssetDict]]
    assignedUsers: Optional[List[TaskUserDict]]
    company: Optional[TaskCompanyDict]
    workspace: WorkspaceDict
