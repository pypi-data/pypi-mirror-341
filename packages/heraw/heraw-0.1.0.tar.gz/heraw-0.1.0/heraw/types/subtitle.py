from typing import TypedDict


class SubtitleDict(TypedDict):
    """Subtitle resource representation."""

    uuid: str
    fileUuid: str
    locale: str
    fileName: str
