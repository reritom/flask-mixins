from flask.views import MethodView

from flask_mixins import JsonifyMixin


def test_tuple_with_dict_ok(app):
    class Index(JsonifyMixin, MethodView):
        def get(self):
            return {"hello": "world"}, 200

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"hello": "world"}


def test_non_tuple_with_dict_ok(app):
    class Index(JsonifyMixin, MethodView):
        def get(self):
            return {"hello": "world"}

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.is_json
    assert response.get_json() == {"hello": "world"}


def test_tuple_with_top_level_list_ok(app):
    class Index(JsonifyMixin, MethodView):
        def get(self):
            return [1, 2, 3], 200

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [1, 2, 3]


def test_non_tuple_with_top_level_list_ok(app):
    class Index(JsonifyMixin, MethodView):
        def get(self):
            return [1, 2, 3]

    app.add_url_rule("/", view_func=Index.as_view("index"))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [1, 2, 3]
