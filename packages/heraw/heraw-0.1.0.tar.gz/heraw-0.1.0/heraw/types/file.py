from typing import TypedDict, Optional, Dict, Any, List, NotRequired


class PartUploadDict(TypedDict):
    """Part upload resource representation."""

    ETag: str
    PartNumber: int
    ChecksumCRC32: NotRequired[str]
    ChecksumCRC32C: NotRequired[str]
    ChecksumSHA1: NotRequired[str]
    ChecksumSHA256: NotRequired[str]


class MultipartUploadDict(TypedDict):
    """Multipart upload resource representation."""

    uploadId: str
    parts: List[PartUploadDict]


class FileDict(TypedDict):
    """File resource representation."""

    uuid: str
    name: str
    mimeType: str
    size: int
    version: int
    folderUuid: str
    status: Optional[str]
    created: str
    updated: str
    uploadGroup: Optional[str]
    customFields: Optional[Dict[str, Any]]


class FileAssetDict(TypedDict):
    """File asset resource representation."""

    uuid: str
    url: str
    version: int
    collection_id: int
    url_expires: str
    format: str
    mime_type: str
    exif_result: Optional[Dict[str, Any]]
    type: str
    quality: str
    size: int
    key: str
    name: str
    metadata: Optional[Dict[str, Any]]
    status: str
    created: str
    bucketName: str
    subtitleUuid: Optional[str]
    exifResult: Optional[Dict[str, Any]]
    mimeType: str
    updated: str
    collectionId: int


class FileCreateResponseLinksDict(TypedDict):
    """File create response links resource representation."""

    part: int
    url: str
    size: int


class FileCreateResponseDict(TypedDict):
    """File create response resource representation."""

    uploadId: str
    file: FileDict
    links: List[FileCreateResponseLinksDict]
    asset: FileAssetDict


class CompleteMultipartUploadDict(TypedDict):
    """Complete multipart upload resource representation."""

    uploadId: str
    parts: List[PartUploadDict]


class FileUploadDict(TypedDict):
    """File upload resource representation."""

    name: NotRequired[str]
    mimeType: NotRequired[str]
    size: NotRequired[int]
    folderUuid: str
    uploadGroup: str
    customFields: NotRequired[Dict[str, Any]]
