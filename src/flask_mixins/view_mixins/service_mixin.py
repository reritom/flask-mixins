from __future__ import annotations

from typing import Any, Dict


class ServiceMixin:
    service_class = None

    def get_service_options(self, *args, **kwargs) -> Dict[Any, Any]:
        # Can be overridden
        return {}

    def get_service(self, *args, **kwargs) -> Any:
        # Can be overridden
        if not self.service_class:
            raise RuntimeError("Unable to get service with no service_class defined")

        service_class: type[Any] = self.service_class
        service_options = self.get_service_options(*args, **kwargs)
        service_options.update(**kwargs)
        return service_class(*args, **service_options)
