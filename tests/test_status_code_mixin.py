import pytest
from flask.views import MethodView

from flask_mixins import StatusCodeMixin


def test_status_code_returns_unaffected(app):
    class Index(StatusCodeMixin, MethodView):
        def get(self):
            return "hey", 201

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    assert client.get("/").status_code == 201


def test_status_code_204_if_none(app):
    class Index(StatusCodeMixin, MethodView):
        def get(self):
            return {}

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    assert client.get("/").status_code == 204


@pytest.mark.parametrize(
    ("method,expected_status_code"),
    [("get", 200), ("post", 201), ("patch", 200), ("delete", 200), ("put", 200)],
)
def test_implicit_status_codes(app, method, expected_status_code):
    Index = type(
        "View",
        (
            StatusCodeMixin,
            MethodView,
        ),
        {method: lambda self: method},
    )
    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    assert getattr(client, method)("/").status_code == expected_status_code
