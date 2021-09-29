import pytest

from flask_mixins import ServiceMixin


class _Service:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def test_get_service_with_options(app):
    class _View(ServiceMixin):
        service_class = _Service

        def get_service_options(self, *args, **kwargs):
            return {"hello": "world"}

    instance = _View()
    service = instance.get_service()
    assert isinstance(service, _Service)
    assert service.kwargs == {"hello": "world"}


def test_get_service_with_kwargs(app):
    class _View(ServiceMixin):
        service_class = _Service

    instance = _View()
    service = instance.get_service(hello="world")
    assert isinstance(service, _Service)
    assert service.kwargs == {"hello": "world"}


def test_get_service_with_kwargs_and_options(app):
    class _View(ServiceMixin):
        service_class = _Service

        def get_service_options(self, *args, **kwargs):
            return {"hello": "world"}

    instance = _View()
    service = instance.get_service(other="option")
    assert isinstance(service, _Service)
    assert service.kwargs == {"hello": "world", "other": "option"}


def test_get_service_with_kwargs_and_options_overlap_kwargs_prioritised(app):
    class _View(ServiceMixin):
        service_class = _Service

        def get_service_options(self, *args, **kwargs):
            return {"hello": "world"}

    instance = _View()
    service = instance.get_service(hello="this")
    assert isinstance(service, _Service)
    assert service.kwargs == {"hello": "this"}


def test_get_service_no_service_defined(app):
    class _View(ServiceMixin):
        pass

    instance = _View()
    with pytest.raises(RuntimeError):
        instance.get_service()
