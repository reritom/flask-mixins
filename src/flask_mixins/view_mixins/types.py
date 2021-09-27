from __future__ import annotations

from typing import Optional, Tuple, Union

from flask import Response

# TODO Use type alias when py3.10
DictOrList = Union[dict, list]

DictOrListOrResponse = Union[dict, list, Response]

DictOrListOrResponseOrNone = Union[dict, list, Response, None]

DictOrListWithOptionalStatusCodeOrNone = Optional[
    Union[Tuple[DictOrList, int], DictOrList]
]

DictOrListWithOptionalStatusCode = Union[Tuple[DictOrList, int], DictOrList]

DictOrListWithStatusCode = Tuple[DictOrList, int]

DictOrListOrResponseWithStatusCode = Tuple[DictOrListOrResponse, int]

OptionalDictOrListWithStatusCode = Tuple[Optional[DictOrList], int]

FlaskResponseWithStatusCode = Tuple[Response, int]
