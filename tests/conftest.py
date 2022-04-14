from dataclasses import dataclass

import pytest
from flask import Flask
from marshmallow import Schema, fields


@pytest.fixture
def app():
    app = Flask("Test")
    return app


@pytest.fixture
def schema():
    class ItemSchema(Schema):
        hello = fields.Str()

    return ItemSchema


@pytest.fixture
def schema_dataclass():
    @dataclass
    class ItemDataclass:
        hello: str

    return ItemDataclass
