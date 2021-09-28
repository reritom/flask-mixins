from __future__ import annotations

from typing import TYPE_CHECKING

from flask import jsonify, request

if TYPE_CHECKING:
    from flask.views import MethodView

    _Base = MethodView
else:
    _Base = object


_METHOD_CODES = {"post": 201, "get": 200, "delete": 204}


class JsonifyMixin(_Base):
    def dispatch_request(self, *args, **kwargs):
        """
        Jsonify the dict or list of items in the response
        """
        response = super().dispatch_request(*args, **kwargs)
        assert isinstance(response, tuple)

        if response[0] is None:
            response = ({}, response[1])

        assert isinstance(response[0], dict) or isinstance(response[0], list)
        return jsonify(response[0]), response[1]


class StatusCodeMixin(_Base):
    def dispatch_request(self, *args, **kwargs):
        """
        If the response has no status code, supplement it
        """
        method = request.method.lower()
        status = _METHOD_CODES.get(method, 200)
        response = super().dispatch_request(*args, **kwargs)

        if not isinstance(response, tuple):
            # Infer the status code
            response = response, status if response else 204

        return response
