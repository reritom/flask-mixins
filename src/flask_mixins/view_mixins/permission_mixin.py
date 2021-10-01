from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Protocol

from ._utils import method

if TYPE_CHECKING:
    from flask.views import MethodView

    _Base = MethodView
else:
    _Base = object


class PermissionProtocol(Protocol):
    def __init__(self, *args, **kwargs):
        ...

    def check_permission(self):
        """Check that the permission is satisfied"""


class PermissionMixin(_Base):
    def _get_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return getattr(self, "permissions", [])

    def get_write_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return self._get_permissions()

    def get_read_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return self._get_permissions()

    def get_post_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return self.get_write_permissions()

    def get_put_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return self.get_write_permissions()

    def get_patch_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return self.get_write_permissions()

    def get_delete_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return self.get_write_permissions()

    def get_get_permissions(self) -> Iterable[type[PermissionProtocol]]:
        return self.get_read_permissions()

    def get_permissions(self) -> Iterable[type[PermissionProtocol]]:
        if method_ := getattr(self, f"get_{method()}_permissions", None):
            return method_()
        return self._get_permissions()

    def dispatch_request(self, *args, **kwargs) -> Any:
        for permission in self.get_permissions():
            permission().check_permission()

        return super().dispatch_request(*args, **kwargs)
