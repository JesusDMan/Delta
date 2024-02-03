import pytest

from smart_delta.src.delta_applier import DeltaApplier
from smart_delta.src.delta_generator import DeltaGenerator


@pytest.mark.parametrize("data_1,data_2",
                         [("kaka", "kaka"), ("kiki", "kaka"), ("Hi! This is greate", "kiki"), ("kiki", "Hi! This is greate"),
                          ("kaka+", "kiki"), ("kaka", "kiki+"), ("kaka-", "kiki"), ("kaka", "kiki-"), ("kaka-", "kiki+"),
                          ("kaka\\-", "kiki"), ("k+-\\|-+$\\$aka", "kiki+"), (
                                  "ka=-=-00-43=-=-3=-=-=-=-=+_)+_489whgjh;lknf;gjkl;lks;glkf;lknaw4987098742p;ohasg=-=-=-=-+-+_+$_+$_+(*$_ka",
                                  "kiki",), ], )
def test_delta_applier_applies_delta_correctly(data_1, data_2):
    delta_steps = str(DeltaGenerator(data_1, data_2))

    assert DeltaApplier(delta_steps).apply_on_data(data_1) == data_2
    assert DeltaApplier(delta_steps).apply_on_data(data_2, reverse_delta=True) == data_1
