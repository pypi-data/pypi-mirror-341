from typing import TypedDict, Optional, List
from .file import FileDict


class FolderDict(TypedDict):
    """Folder resource representation."""

    uuid: str
    name: str
    parentUuid: Optional[str]
    created: str
    updated: str
    path: str
    isTeamFolder: bool
    isProjectFolder: bool
    contentCount: int


class FolderContentDict(TypedDict):
    """Folder content including files and subfolders."""

    folders: List[FolderDict]
    files: List[FileDict]
