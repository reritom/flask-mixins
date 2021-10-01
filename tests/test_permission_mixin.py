from unittest.mock import patch

import pytest
from flask.views import MethodView

from flask_mixins import PermissionMixin

NO_OP = object()


class _OKPermission:
    def check_permission(self):
        return


class _KOPermission:
    def check_permission(self):
        raise PermissionError()


class ViewOK(_OKPermission):
    pass


class ViewKO(_KOPermission):
    pass


class ReadOK(_OKPermission):
    pass


class WriteOK(_OKPermission):
    pass


class GetOK(_OKPermission):
    pass


class PostOK(_OKPermission):
    pass


class PatchOK(_OKPermission):
    pass


class PutOK(_OKPermission):
    pass


class DeleteOK(_OKPermission):
    pass


class View(PermissionMixin, MethodView):
    permissions = (ViewOK,)


@pytest.mark.parametrize(
    "method,method_permissions,general_method,general_method_permissions,expected_permissions",  # noqa
    [
        # No overrides
        ("get", NO_OP, "read", NO_OP, (ViewOK,)),
        ("post", NO_OP, "write", NO_OP, (ViewOK,)),
        ("put", NO_OP, "write", NO_OP, (ViewOK,)),
        ("patch", NO_OP, "write", NO_OP, (ViewOK,)),
        ("delete", NO_OP, "write", NO_OP, (ViewOK,)),
        # Both override
        ("get", (GetOK,), "read", (ReadOK,), (GetOK,)),
        ("post", (PostOK,), "write", (WriteOK,), (PostOK,)),
        ("put", (PutOK,), "write", (WriteOK,), (PutOK,)),
        ("patch", (PatchOK,), "write", (WriteOK,), (PatchOK,)),
        ("delete", (DeleteOK,), "write", (WriteOK,), (DeleteOK,)),
        # No specific override
        ("get", NO_OP, "read", (ReadOK,), (ReadOK,)),
        ("post", NO_OP, "write", (WriteOK,), (WriteOK,)),
        ("put", NO_OP, "write", (WriteOK,), (WriteOK,)),
        ("patch", NO_OP, "write", (WriteOK,), (WriteOK,)),
        ("delete", NO_OP, "write", (WriteOK,), (WriteOK,)),
        # No general override
        ("get", (GetOK,), "read", NO_OP, (GetOK,)),
        ("post", (PostOK,), "write", NO_OP, (PostOK,)),
        ("put", (PutOK,), "write", NO_OP, (PutOK,)),
        ("patch", (PatchOK,), "write", NO_OP, (PatchOK,)),
        ("delete", (DeleteOK,), "write", NO_OP, (DeleteOK,)),
    ],
)
def test_get_permissions_override_specific_and_general_permissions(
    method,
    method_permissions,
    general_method,
    general_method_permissions,
    expected_permissions,
):
    _dict = {}
    if general_method_permissions is not NO_OP:
        _dict[
            f"get_{general_method}_permissions"
        ] = lambda self: general_method_permissions
    if method_permissions is not NO_OP:
        _dict[f"get_{method}_permissions"] = lambda self: method_permissions

    SubTestView = type(
        "SubTestView",
        (
            View,
            MethodView,
        ),
        _dict,
    )

    with patch("flask_mixins.view_mixins.permission_mixin.method") as method_mock:
        method_mock.return_value = method
        permissions = SubTestView().get_permissions()

    assert permissions == expected_permissions


def test_dispatch_permission_check_ok(app):
    class Index(PermissionMixin, MethodView):
        permissions = (ViewOK,)

        def get(self):
            return {"hello": "world"}

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_dispatch_permission_check_ko(app):
    class Index(PermissionMixin, MethodView):
        permissions = (ViewKO,)

        def get(self):
            return {"hello": "world"}

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 500
