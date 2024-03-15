import pytest

from smart_delta.src.delta_applier import DeltaApplier
from smart_delta.src.delta_generator import DeltaGenerator


@pytest.mark.parametrize("data_0,data_1",
                         [("kaka", "kaka"), ("kiki", "kaka"), ("Hi! This is greate", "kiki"), ("kiki", "Hi! This is greate"),
                          ("kaka+", "kiki"), ("kaka", "kiki+"), ("kaka-", "kiki"), ("kaka", "kiki-"), ("kaka-", "kiki+"),
                          ("kaka\\-", "kiki"), ("k+-\\|-+$\\$aka", "kiki+"), (
                                  "ka=-=-00-43=-=-3=-=-=-=-=+_)+_489whgjh;lknf;gjkl;lks;glkf;lknaw4987098742p;ohasg=-=-=-=-+-+_+$_+$_+(*$_ka",
                                  "kiki",), ], )
def test_delta_applier_applies_delta_correctly(data_0: str, data_1: str):
    data_0 = data_0.encode("utf-8")
    data_1 = data_1.encode("utf-8")
    delta_steps = str(DeltaGenerator(data_0, data_1, 3, 50)).encode("utf-8")

    assert DeltaApplier(delta_steps).apply_on_data(data_0) == data_1
    assert DeltaApplier(delta_steps).apply_on_data(data_1, reverse_delta=True) == data_0
