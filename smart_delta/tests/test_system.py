import pytest

from smart_delta.src.delta_applier import DeltaApplier
from smart_delta.src.delta_generator import DeltaGenerator


@pytest.mark.parametrize(
    "data_0,data_1",
    [
        (b"kaka", b"kaka"),
        (b"kiki", b"kaka"),
        (b"Hi! This is greate", b"kiki"),
        (b"kiki", b"Hi! This is greate"),
        (b"kaka+", b"kiki"),
        (b"kaka", b"kiki+"),
        (b"kaka-", b"kiki"),
        (b"kaka", b"kiki-"),
        (b"kaka-", b"kiki+"),
        (b"kaka\\-", b"kiki"),
        (b"k+-\\|-+$\\$aka", b"kiki+"),
        (
            b"ka=-=-00-43=-=-3=-=-=-=-=+_)+_489whgjh;lknf;gjkl;lks;glkf;lknaw4987098742p;ohasg=-=-=-=-+"
            b"-+_+$_+$_+(*$_ka",
            b"kiki",
        ),
    ],
)
def test_delta_applier_applies_delta_correctly(data_0: bytes, data_1: bytes):
    delta_steps = bytes(DeltaGenerator(data_0, data_1, 3, 50))

    assert DeltaApplier(delta_steps).apply_on_data(data_0) == data_1
    assert DeltaApplier(delta_steps).apply_on_data(data_1, reverse_delta=True) == data_0
