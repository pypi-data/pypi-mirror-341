from typing import TypedDict, Optional


class EntityPictureAssetDict(TypedDict):
    """Entity picture asset."""

    uuid: str
    key: str
    url: str
    urlExpire: Optional[str]
    bucketName: str


class EntityAddressDict(TypedDict):
    """Entity address."""

    street: str
    city: str
    country: str
    zipCode: str


class EntityDict(TypedDict):
    """Entity resource representation."""

    uuid: str
    name: str
    color: str
    phone: str
    address: EntityAddressDict
    pictureAsset: EntityPictureAssetDict
