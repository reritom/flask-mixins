from __future__ import annotations

from typing import Any, Protocol, Type


class ServiceProtocol(Protocol):
    def __init__(self, *args, **kwargs, context: Any):
        ...


class ServiceMixin:
    def get_service_context(self, *args, **kwargs) -> Any:
        # Can be overridden
        return None

    def get_service(self, *args, **kwargs) -> Any:
        # Can be overridden
        try:
            service_class: Type[ServiceProtocol] = self.service
        except AttributeError:
            raise Exception(
                "Unable to get service with no service class defined"
            ) from None

        context = self.get_service_context()
        return service_class(*args, **kwargs, context=context)
