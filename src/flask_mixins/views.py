from __future__ import annotations

from flask import request
from flask.views import MethodView

from .view_mixins import (
    JsonifyMixin,
    PermissionMixin,
    SchemaMixin,
    ServiceMixin,
    StatusCodeMixin,
)


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
