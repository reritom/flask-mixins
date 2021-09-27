from __future__ import annotations

from typing import TYPE_CHECKING, Union

from flask import jsonify, request

if TYPE_CHECKING:
    from .types import (
        DictOrListOrResponse,
        DictOrListOrResponseWithStatusCode,
        FlaskResponseWithStatusCode,
        OptionalDictOrListWithStatusCode,
    )


_METHOD_CODES = {"post": 201, "get": 200, "delete": 204}


class JsonifyMixin:
    def dispatch_request(self, *args, **kwargs) -> FlaskResponseWithStatusCode:
        """
        Jsonify the dict or list of items in the response
        """
        response: OptionalDictOrListWithStatusCode = super().dispatch_request(
            *args, **kwargs
        )
        assert isinstance(response, tuple)

        if response[0] is None:
            response = ({}, response[1])

        assert isinstance(response[0], dict) or isinstance(response[0], list)
        return jsonify(response[0]), response[1]


class StatusCodeMixin:
    def dispatch_request(self, *args, **kwargs) -> DictOrListOrResponseWithStatusCode:
        """
        If the response has no status code, supplement it
        """
        method = request.method.lower()
        status = _METHOD_CODES.get(method, 200)

        response: Union[
            DictOrListOrResponseWithStatusCode,
            DictOrListOrResponse,
        ]
        response = super().dispatch_request(*args, **kwargs)

        if not isinstance(response, tuple):
            # Infer the status code
            response = response, status if response else 204

        return response
