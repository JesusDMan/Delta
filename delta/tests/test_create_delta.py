import pytest

from backup_syncer.modules.delta.create_delta import *


@pytest.mark.parametrize("data_1,data_2", [
    ("kaka", "kaka"),
    ("kiki", "kaka"),
    ("Hi! This is greate", "kiki"),
    ("kiki", "Hi! This is greate"),
    ("kaka+", "kiki"),
    ("kaka", "kiki+"),
    ("kaka-", "kiki"),
    ("kaka", "kiki-"),
    ("kaka-", "kiki+"),
    ("kaka\\-", "kiki"),
    ("k+-\\|-+$\\$aka", "kiki+"),
    ("ka=-=-00-43=-=-3=-=-=-=-=+_)+_489whgjh;lknf;gjkl;lks;glkf;lknaw4987098742p;ohasg=-=-=-=-+-+_+$_+$_+(*$_ka", "kiki"),
])
def test_shit(data_1, data_2):
    delta_list = create_delta_steps_list(data_1, data_2)
    delta = create_delta_string(delta_list)

    assert apply_delta.apply_string_delta(data_1, delta) == data_2
    assert apply_delta.apply_string_delta(data_2, delta, reverse_delta=True) == data_1
