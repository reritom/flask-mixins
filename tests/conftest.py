import pytest
from flask import Flask


@pytest.fixture
def app():
    app = Flask("Test")
    return app
