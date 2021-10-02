import pytest

from flask_mixins import BasePermission


class _OKPermission(BasePermission):
    def check_permission(self):
        return


class _KOPermission(BasePermission):
    error_message = "KO permission"

    def check_permission(self):
        raise PermissionError(self.error_message)


class OK1(_OKPermission):
    pass


class OK2(_OKPermission):
    pass


class OK3(_OKPermission):
    pass


class KO1(_KOPermission):
    error_message = "KO1"


class KO2(_KOPermission):
    error_message = "KO2"


class KO3(_KOPermission):
    error_message = "KO3"


@pytest.mark.parametrize(
    "permission",
    [
        # With types
        (OK1 & OK2),
        (OK1 & OK2 & OK3),
        (OK1 | KO1),
        (KO1 | OK1),
        (KO1 | KO2 | OK1),
        (OK1 & (KO1 | OK2)),
        # With types and instances
        (OK1() & OK2),
        (OK1 & OK2() & OK3()),
        (OK1 | KO1()),
        (KO1 | OK1()),
        (KO1() | KO2 | OK1),
        (OK1() & (KO1 | OK2())),
    ],
)
def test_permissions_ok(permission):
    try:
        permission.check_permission()
    except PermissionError:
        pytest.fail("Permission check failed")


@pytest.mark.parametrize(
    "permission,message",
    [
        # With types
        (OK1 & KO1, "KO1"),
        (KO1 & KO2 & OK1, "KO1"),
        (OK1 & OK2 & KO3, "KO3"),
        (KO1 | KO2, "KO1"),
        (KO1 & (OK1 | OK2), "KO1"),
        (OK1 & (OK1 & KO1), "KO1"),
        # With types and instances
        (OK1() & KO1, "KO1"),
        (KO1 & KO2() & OK1, "KO1"),
        (OK1 & OK2 & KO3(), "KO3"),
        (KO1 | KO2(), "KO1"),
        (KO1() & (OK1 | OK2), "KO1"),
        (OK1 & (OK1() & KO1()), "KO1"),
    ],
)
def test_permissions_ko(permission, message):
    with pytest.raises(PermissionError) as ctx:
        permission.check_permission()

    assert repr(ctx.value) == f"PermissionError('{message}')"
