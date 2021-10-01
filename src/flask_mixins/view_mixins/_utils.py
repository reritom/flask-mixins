from flask import request


def method() -> str:
    return request.method.lower()
