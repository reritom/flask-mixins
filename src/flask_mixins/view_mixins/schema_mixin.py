from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type, Union

from flask import request

if TYPE_CHECKING:
    from app.shared.tools.view_mixins.types import (
        DictOrListWithOptionalStatusCode,
        DictOrListWithOptionalStatusCodeOrNone,
    )
    from marshmallow import Schema


class _FilterSchemaMixin:
    def get_filter_schema_class(self) -> Type[Schema]:
        # Can be overridden
        try:
            return self.filter_schema
        except AttributeError:
            raise Exception("No filter schema defined for the class")

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
            context=self.get_filter_schema_context(),
            **self.get_filter_schema_options()
        )

    def get_filter_data(self) -> Union[dict, Any]:
        return self.get_filter_schema_instance().load(request.args.to_dict())


class _ResponseSchemaMixin:
    def get_response_schema_class(self, *args, **kwargs) -> Type[Schema]:
        # Can be overridden
        try:
            schema = self.response_schema
        except AttributeError:
            schema = None

        if schema:
            return schema

        try:
            return self.schema
        except AttributeError:
            raise Exception("No response schema defined in the class") from None

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
            **self.get_response_schema_options()
        )

    @property
    def _many_response(self) -> bool:
        return self.get_response_schema_options().get("many", False)

    def dispatch_request(self, *args, **kwargs) -> DictOrListWithOptionalStatusCode:
        """
        Convert the response to a dict or list of dicts using the response schema
        if there is a response object. Keep the status code if there is one, and
        return an empty dictionary if the given object is None
        """
        response: DictOrListWithOptionalStatusCodeOrNone
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
                raise Exception("View returned list, but expected an individual item")
            if should_be_many and not isinstance(response, list):
                raise Exception(
                    "View returned non-list, but expected list"
                )

            obj = schema.dump(response)

        return (obj, response[1]) if tuple_response else obj


class _RequestSchemaMixin:
    def get_request_schema_context(self) -> dict:
        # Can be overridden
        return {}

    def get_request_schema_options(self) -> dict:
        # Can be overridden
        return {}

    def get_response_schema_class(self, *args, **kwargs) -> Type[Schema]:
        # Can be overridden
        try:
            schema = self.request_schema
        except AttributeError:
            schema = None

        if schema:
            return schema

        try:
            return self.schema
        except AttributeError:
            raise Exception("No request schema defined in the class") from None

    def get_request_schema_instance(self) -> Schema:
        class_ = self.get_request_schema_class()
        return class_(
            context=self.get_request_schema_context(),
            **self.get_request_schema_options()
        )

    def get_patch_schema_class(self) -> Type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_patch_schema_context(self) -> {}:
        # Can be overridden
        return self.get_request_schema_context()

    def get_patch_schema_options(self) -> {}:
        # Can be overridden
        return self.get_request_schema_options()

    def get_patch_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_patch_schema_class()
        return class_(
            context=self.get_patch_schema_context(),
            **self.get_patch_schema_options()
        )

    def get_post_schema_class(self) -> Type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_post_schema_context(self) -> {}:
        # Can be overridden
        return self.get_request_schema_context()

    def get_post_schema_options(self) -> {}:
        # Can be overridden
        return self.get_request_schema_options()

    def get_post_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_post_schema_class()
        return class_(
            context=self.get_post_schema_context(),
            **self.get_post_schema_options()
        )

    def get_put_schema_class(self) -> Type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_put_schema_context(self) -> {}:
        # Can be overridden
        return self.get_request_schema_context()

    def get_put_schema_options(self) -> {}:
        # Can be overridden
        return self.get_request_schema_options()

    def get_put_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_put_schema_class()
        return class_(
            context=self.get_put_schema_context(),
            **self.get_put_schema_options()
        )

    def get_get_schema_class(self) -> Type[Schema]:
        # Can be overridden
        return self.get_request_schema_class()

    def get_get_schema_context(self) -> {}:
        # Can be overridden
        return self.get_request_schema_context()

    def get_get_schema_options(self) -> {}:
        # Can be overridden
        return self.get_request_schema_options()

    def get_get_schema_instance(self) -> Schema:
        # Can be overridden
        class_ = self.get_get_schema_class()
        return class_(
            context=self.get_get_schema_context(),
            **self.get_get_schema_options()
        )

    def _get_request_schema_instance(self) -> Schema:
        method = request.method.lower()
        if method_ := getattr(self, f"get_{method}_schema_instance", None):
            return method_()
        return self.get_request_schema_instance()

    def get_validated_data(self) -> Union[dict, Any]:
        return self._get_request_schema_instance().load(request.get_json())


class SchemaMixin(_RequestSchemaMixin, _ResponseSchemaMixin, _FilterSchemaMixin):
    pass
