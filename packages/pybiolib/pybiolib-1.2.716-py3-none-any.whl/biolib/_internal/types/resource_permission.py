from .typing import TypedDict


class ResourcePermissionDict(TypedDict):
    uuid: str
    created_at: str
    action: str
    resource_uuid: str
    target_resource_uuid: str


class ResourcePermissionDetailedDict(ResourcePermissionDict):
    pass
