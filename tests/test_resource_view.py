from flask import jsonify

from flask_mixins import ResourceView


def test_tuple_with_werkzeug_response_ok(app, schema):
    class Index(ResourceView):
        response_schema = schema

        def get(self):
            return jsonify({"hello": "world"}), 200

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"hello": "world"}


def test_ko_multiple_items_returned(app, schema, schema_dataclass):
    class Index(ResourceView):
        response_schema = schema

        def get(self):
            return [schema_dataclass(hello="world")], 200

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 500


def test_ok_with_status_code(app, schema, schema_dataclass):
    class Index(ResourceView):
        response_schema = schema

        def get(self):
            return schema_dataclass(hello="world"), 200

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"hello": "world"}


def test_ok_without_status_code(app, schema, schema_dataclass):
    class Index(ResourceView):
        response_schema = schema

        def get(self):
            return schema_dataclass(hello="world")

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"hello": "world"}
