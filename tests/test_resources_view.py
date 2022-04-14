from flask import jsonify

from flask_mixins import ResourcesView


def test_tuple_with_werkzeug_response_ok(app, schema):
    class Index(ResourcesView):
        response_schema = schema

        def get(self):
            return jsonify({"hello": "world"}), 200

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"hello": "world"}


def test_ko_single_item_returned(app, schema, schema_dataclass):
    class Index(ResourcesView):
        response_schema = schema

        def get(self):
            return schema_dataclass(hello="world")

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 500


def test_ok_with_status_code(app, schema, schema_dataclass):
    class Index(ResourcesView):
        response_schema = schema

        def get(self):
            return [
                schema_dataclass(hello="world"),
                schema_dataclass(hello="earth"),
            ], 200

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    print(response.get_json())
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"hello": "world"}, {"hello": "earth"}]


def test_ok_without_status_code(app, schema, schema_dataclass):
    class Index(ResourcesView):
        response_schema = schema

        def get(self):
            return [schema_dataclass(hello="world"), schema_dataclass(hello="earth")]

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"hello": "world"}, {"hello": "earth"}]
