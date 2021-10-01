from __future__ import annotations

from typing import TYPE_CHECKING

from flask import jsonify

from ._utils import method

if TYPE_CHECKING:
    from flask.views import MethodView

    _Base = MethodView
else:
    _Base = object


class JsonifyMixin(_Base):
    def dispatch_request(self, *args, **kwargs):
        """
        Jsonify the dict or list of items in the response
        """
        response = super().dispatch_request(*args, **kwargs)

        if isinstance(response, tuple):
            if response[0] is None:
                response = ({}, response[1])

            if isinstance(response[0], dict) or isinstance(response[0], list):
                return jsonify(response[0]), response[1]

        if isinstance(response, dict) or isinstance(response, list):
            return jsonify(response)

        return response


class StatusCodeMixin(_Base):
    def dispatch_request(self, *args, **kwargs):
        """
        If the response has no status code, supplement it
        """
        status = 201 if method() == "post" else 200
        response = super().dispatch_request(*args, **kwargs)

        if not isinstance(response, tuple):
            # Infer the status code
            response = response, status if response else 204

        return response
