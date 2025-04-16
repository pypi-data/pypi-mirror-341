from typing import TypedDict, Optional


class CastDict(TypedDict):
    """Cast resource representation."""

    uuid: str
    name: str
    download: bool
    comment: bool
    expires: Optional[str]
    maxViews: int
    projectUuid: str
    backgroundColor: str
    textColor: str
    folderUuid: str
