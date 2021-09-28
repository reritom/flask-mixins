from __future__ import annotations

from typing import Any, Protocol


class ServiceProtocol(Protocol):
    def __init__(self, *args, context: Any, **kwargs):
        ...


class ServiceMixin:
    service = None

    def get_service_context(self, *args, **kwargs) -> Any:
        # Can be overridden
        return None

    def get_service(self, *args, **kwargs) -> Any:
        # Can be overridden
        if not self.service:
            raise Exception("Unable to get service with no service class defined")

        service_class: type[ServiceProtocol] = self.service
        context = self.get_service_context()
        return service_class(*args, **kwargs, context=context)
