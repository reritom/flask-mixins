from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flask import request

from ._utils import method

if TYPE_CHECKING:
    from marshmallow import Schema


if TYPE_CHECKING:
    from flask.views import MethodView

    _Base = MethodView
else:
    _Base = object


class _FilterSchemaMixin:
    filter_schema = None

    def get_filter_schema_class(self) -> type[Schema]:
        # Can be overridden
        if not self.filter_schema:
            raise RuntimeError("No filter schema defined for the class")

        return self.filter_schema

    def get_filter_schema_context(self) -> dict:
        # Can be overridden
        return {}

    def get_filter_schema_options(self) -> dict:
        # Can be overridden
        return {}

    def get_filter_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_filter_schema_class()
        return class_(
            context=self.get_filter_schema_context(), **self.get_filter_schema_options()
        )

    def get_filter_data(self) -> dict | Any:
        return self.get_filter_schema_instance().load(request.args.to_dict())


class _ResponseSchemaMixin(_Base):
    schema = None
    response_schema = None

    def get_response_schema_class(self, *args, **kwargs) -> type[Schema]:
        # Can be overridden
        if schema := self.response_schema:
            return schema

        if not self.schema:
            raise RuntimeError("No response schema defined in the class")

        return self.schema

    def get_response_schema_context(self) -> dict:
        # Can be overridden
        return {}

    def get_response_schema_options(self) -> dict:
        # Can be overridden
        return {}

    def get_response_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_response_schema_class()
        return class_(
            context=self.get_response_schema_context(),
            **self.get_response_schema_options(),
        )

    @property
    def _many_response(self) -> bool:
        return self.get_response_schema_options().get("many", False)

    def dispatch_request(self, *args, **kwargs):
        """
        Convert the response to a dict or list of dicts using the response schema
        if there is a response object. Keep the status code if there is one, and
        return an empty dictionary if the given object is None
        """
        response = super().dispatch_request(*args, **kwargs)

        if response is None:
            return {}

        schema = self.get_response_schema_instance()
        tuple_response = isinstance(response, tuple)
        obj = response[0] if tuple_response else response
        should_be_many = self._many_response
        should_be_single = not should_be_many

        if not isinstance(response, dict):
            if should_be_single and isinstance(response, list):
                raise RuntimeError(
                    "View returned list, but expected an individual item"
                )
            if should_be_many and not isinstance(response, list):
                raise RuntimeError("View returned non-list, but expected list")

            obj = schema.dump(response)

        return (obj, response[1]) if tuple_response else obj


class _RequestSchemaMixin:
    request_schema = None
    schema = None

    def get_request_schema_context(self) -> dict:
        # Can be overridden
        return {}

    def get_request_schema_options(self) -> dict:
        # Can be overridden
        return {}

    def get_request_schema_class(self, *args, **kwargs) -> type[Schema]:
        # Can be overridden
        if schema := self.request_schema:
            return schema

        if not self.schema:
            raise RuntimeError("No request schema defined in the class")

        return self.schema

    def get_request_schema_instance(self) -> Schema:
        class_ = self.get_request_schema_class()
        return class_(
            context=self.get_request_schema_context(),
            **self.get_request_schema_options(),
        )

    def get_patch_schema_class(self) -> type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_patch_schema_context(self) -> dict:
        # Can be overridden
        return self.get_request_schema_context()

    def get_patch_schema_options(self) -> dict:
        # Can be overridden
        return self.get_request_schema_options()

    def get_patch_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_patch_schema_class()
        return class_(
            context=self.get_patch_schema_context(), **self.get_patch_schema_options()
        )

    def get_post_schema_class(self) -> type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_post_schema_context(self) -> dict:
        # Can be overridden
        return self.get_request_schema_context()

    def get_post_schema_options(self) -> dict:
        # Can be overridden
        return self.get_request_schema_options()

    def get_post_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_post_schema_class()
        return class_(
            context=self.get_post_schema_context(), **self.get_post_schema_options()
        )

    def get_put_schema_class(self) -> type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_put_schema_context(self) -> dict:
        # Can be overridden
        return self.get_request_schema_context()

    def get_put_schema_options(self) -> dict:
        # Can be overridden
        return self.get_request_schema_options()

    def get_put_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_put_schema_class()
        return class_(
            context=self.get_put_schema_context(), **self.get_put_schema_options()
        )

    def get_get_schema_class(self) -> type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_get_schema_context(self) -> dict:
        # Can be overridden
        return self.get_request_schema_context()

    def get_get_schema_options(self) -> dict:
        # Can be overridden
        return self.get_request_schema_options()

    def get_get_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_get_schema_class()
        return class_(
            context=self.get_get_schema_context(), **self.get_get_schema_options()
        )

    def _get_request_schema_instance(self) -> Schema:
        if method_ := getattr(self, f"get_{method()}_schema_instance", None):
            return method_()
        return self.get_request_schema_instance()

    def get_validated_data(self) -> dict | Any:
        data = request.get_json()
        if data is not None:
            return self._get_request_schema_instance().load(data)
        return {}


class SchemaMixin(_RequestSchemaMixin, _ResponseSchemaMixin, _FilterSchemaMixin):
    pass
