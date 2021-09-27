from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Protocol

from flask import request

def method():
    return request.method.lower()


class PermissionProtocol(Protocol):
    def check_permission(self):
        """Check that the permission is satisfied"""


class PermissionMixin:
    def _get_permissions(self) -> List[PermissionProtocol]:
        return getattr(self, "permissions", [])

    def get_write_permissions(self) -> List[PermissionProtocol]:
        return self._get_permissions()

    def get_read_permissions(self) -> List[PermissionProtocol]:
        return self._get_permissions()

    def get_post_permissions(self) -> List[PermissionProtocol]:
        return self.get_write_permissions()

    def get_put_permissions(self) -> List[PermissionProtocol]:
        return self.get_write_permissions()

    def get_patch_permissions(self) -> List[PermissionProtocol]:
        return self.get_write_permissions()

    def get_delete_permissions(self) -> List[PermissionProtocol]:
        return self.get_write_permissions()

    def get_get_permissions(self) -> List[PermissionProtocol]:
        return self.get_read_permissions()

    def get_permissions(self) -> List[PermissionProtocol]:
        if methind_ := getattr(self, f"get_{method()}_permissions", None):
            return method_()
        return self._get_permissions()

    def dispatch_request(self, *args, **kwargs) -> Any:
        for permission in self.get_permissions():
            permission().check_permission()

        return super().dispatch_request(*args, **kwargs)
