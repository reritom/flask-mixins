from __future__ import annotations


class PermissionType(type):
    def __or__(self, other: BasePermission | type[BasePermission]) -> BasePermission:
        return Or(self, other)

    def __and__(self, other: BasePermission | type[BasePermission]) -> BasePermission:
        return And(self, other)


class BasePermission(metaclass=PermissionType):
    def check_permission(self):
        raise NotImplementedError

    def __or__(self, other: BasePermission | type[BasePermission]) -> BasePermission:
        return Or(self, other)

    def __and__(self, other: BasePermission | type[BasePermission]) -> BasePermission:
        return And(self, other)

    def __call__(self) -> BasePermission:
        return self


class Permission(BasePermission):
    def has_permission(self) -> bool:
        ...

    @property
    def error_message(self) -> str:
        ...

    def check_permission(self):
        if not self.has_permission():
            raise PermissionError(self.error_message)


class Or(BasePermission):
    def __init__(self, *args: tuple[BasePermission | type[BasePermission], ...]):
        self.permissions = args

    def check_permission(self) -> bool:
        errors = []
        for permission in self.permissions:
            try:
                return permission().check_permission()
            except PermissionError as e:
                errors.append(e)
                continue

        if errors:
            raise errors[0] from None


class And(BasePermission):
    def __init__(self, *args: tuple[BasePermission | type[BasePermission], ...]):
        self.permissions = args

    def check_permission(self):
        for permission in self.permissions:
            try:
                permission().check_permission()
            except PermissionError:
                raise
