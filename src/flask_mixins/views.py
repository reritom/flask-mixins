from __future__ import annotations

from .view_mixins import (
    JsonifyMixin,
    PermissionMixin,
    SchemaMixin,
    ServiceMixin,
    StatusCodeMixin,
)
from flask.views import MethodView


class _BaseView(
    JsonifyMixin,
    ServiceMixin,
    StatusCodeMixin,
    SchemaMixin,
    PermissionMixin,
    MethodView,
):
    pass


class ResourceView(_BaseView):
    pass


class ResourcesView(_BaseView):
    def get_response_schema_options(self) -> dict:
        return {"many": request.method.lower() == "get"}
