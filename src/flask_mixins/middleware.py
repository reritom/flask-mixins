from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask


class BaseMiddleware:
    def __init__(self, app: Flask | None = None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    def before_request(self):
        pass

    def after_request(self, response):
        return response
