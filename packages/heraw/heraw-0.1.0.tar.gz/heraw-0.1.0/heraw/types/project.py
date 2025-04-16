from typing import TypedDict, Optional, List
from .task import TaskDict
from .workspace import WorkspaceDict


class TeamMemberDict(TypedDict):
    """Team member"""

    uuid: str
    email: str
    firstname: str
    lastname: str
    firm: str
    role: str
    phone: str
    city: str
    country: str
    picture: str
    canExport: bool
    canDownload: bool
    workspaces: List[WorkspaceDict]


class TeamDict(TypedDict):
    """Team information."""

    uuid: str
    name: str
    color: Optional[str]
    castTeamAccess: Optional[bool]
    members: List[TeamMemberDict]
    status: str


class ProjectTeamDict(TypedDict):
    """Project team information."""

    uuid: str
    name: str


class ProjectTaskCountsDict(TypedDict):
    """Project task counts."""

    projectUuid: str
    toDo: int
    inProgress: int
    toValidate: int
    done: int


class ProjectCompanyDict(TypedDict):
    """Project company information."""

    uuid: str
    name: str
    color: str


class ProjectDict(TypedDict):
    """Project resource representation based on the Heraw API."""

    uuid: str
    name: str
    startDate: Optional[str]
    endDate: Optional[str]
    created: str
    updated: str
    status: str
    folderUuid: str
    castsDisabled: bool
    hasCast: bool
    hasStats: bool
    user: str
    company: Optional[ProjectCompanyDict]
    role: Optional[str]
    isFavorite: bool
    color: str
    logoUrl: Optional[str]
    backgroundUrl: Optional[str]
    size: int
    hasNotificationSettings: bool
    team: Optional[ProjectTeamDict]
    taskCounts: Optional[ProjectTaskCountsDict]


class ProjectDetailDict(ProjectDict):
    """Project detail information."""

    tasks: Optional[List[TaskDict]]
