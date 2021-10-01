from distutils.version import LooseVersion

from .view_mixins.misc_mixins import JsonifyMixin, StatusCodeMixin
from .view_mixins.permission_mixin import PermissionMixin
from .view_mixins.schema_mixin import SchemaMixin
from .view_mixins.service_mixin import ServiceMixin
from .views import ResourcesView, ResourceView

__all__ = [
    "JsonifyMixin",
    "StatusCodeMixin",
    "PermissionMixin",
    "SchemaMixin",
    "ServiceMixin",
    "ResourceView",
    "ResourcesView",
]

__version__ = "0.0.2"
__version_info__ = tuple(LooseVersion(__version__).version)
