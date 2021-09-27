# flask-mixins
A collection of mixins to use with Flask to facilitate a cleaner architecture.

## SchemaMixin
The `SchemaMixin` is a way of abstracting some of the logic for validating and accessing the payload data and any query (filter) data, while handling the serialisation of the returned objects into json, using [Marshmallow](https://github.com/marshmallow-code/marshmallow).

The SchemaMixin isn't meant to compete with [Flask Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) as such. It is a different approach with different priorities. The SchemaMixin is just a mixin, so it doesn't support any hyperlinking logic.

What the SchemaMixin does allow is:
- The request schema to be defined on the MethodView, and provides a utility `self.get_validated_data()` that returns the data having been validated against the defined request schema. The request schema might vary (a POST request might require a specific schema for creating the object, while a PATCH request might require another schema). So inspired by [Django Rest Framework](https://www.django-rest-framework.org/), there are a handful of methods that can be overridden to allow the schemas to be dynamic (check the diagram below).
- A filter schema can be defined, that is used by the utility `self.get_filter_data()`, allowing the filter args to be validated against a dedicated marshmallow schema.
- The `dispatch_request` is overridden so that if a non-dictionary object is returned, the object will be dumped using the provided schema, again with multiple options for overriding methods to make the schema dynamic.

![SchemaMixin methods](./docs/diagrams/schema_mixin_funcs.drawio.png)

...

## PermissionMixin
...

## StatusCodeMixin
...

## JsonifyMixin
...

## ResourceMixin
...

## ResourcesMixin
...
