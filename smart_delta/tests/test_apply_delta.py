import pytest

from smart_delta.src.delta_applier import DeltaApplier
from smart_delta.src.delta_element import DeltaElement
from smart_delta.src.delta_generator import DeltaGenerator


@pytest.mark.parametrize("delta_string,parsed_delta_steps",
    [("+1|lala", ["+1|lala"]), ("-1|lala", ["-1|lala"]), ("%1|lala$lili", ["%1|lala$lili"]),
        ("+1|lala+4|lili", ["+1|lala", "+4|lili"]), ("+1|lala\\\\+4|lili", ["+1|lala\\\\", "+4|lili"]),
        ("-1|lala-4|lili", ["-1|lala", "-4|lili"]), ("%1|lala$lili%4|lili$lala", ["%1|lala$lili", "%4|lili$lala"]), (
            "%6|dd my\\$\\-=\\$\\$\\|\\|=\\-\\\\\\$\\+\\|\\| n\\+$my n%18|\\-$\\+_\\+_\\$\\+_\\+=\\-=\\-=\\-=%39|ce\\\\na  this is yayyyy$ron goron",
            ["%6|dd my\\$\\-=\\$\\$\\|\\|=\\-\\\\\\$\\+\\|\\| n\\+$my n", "%18|\\-$\\+_\\+_\\$\\+_\\+=\\-=\\-=\\-=",
                "%39|ce\\\\na  this is yayyyy$ron goron", ],), ], )
def test_parse_delta_steps(delta_string, parsed_delta_steps):
    assert DeltaApplier(delta_string).delta_elements == parsed_delta_steps


@pytest.mark.parametrize("base_data,delta,data_with_delta",
    [("Hi| Duck", ("%", 2, "|", "!"), "Hi! Duck"), ("Hi! Duck", ("%", 2, "!", "|"), "Hi| Duck"),
        ("Hi! Duck", ("+", 8, "er"), "Hi! Ducker"), ("Hi! Ducker", ("-", 8, "er"), "Hi! Duck"),
        ("Hi! I'm a Duck", ("-", 4, "I'm a "), "Hi! Duck"), ("Hi! Duck", ("+", 4, "I'm a "), "Hi! I'm a Duck"),
        ("Hi! This is a Duck", ("%", 4, "This is", "I'm"), "Hi! I'm a Duck"),
        ("Hi! Duck", ("+", 4, "+-|$% "), "Hi! +-|$% Duck"),
        ("Hi! +-|$% Duck", ("%", 4, "+-|$%", "|%$-+"), "Hi! |%$-+ Duck"), ], )
def test_apply_delta_step(base_data, delta, data_with_delta):
    delta = DeltaElement(*delta)
    assert delta.apply_on_data(base_data=base_data)[0] == data_with_delta
    assert (delta.apply_on_data(base_data=data_with_delta, apply_on_reverse=True)[0] == base_data)


@pytest.mark.parametrize("data_1,data_2",
    [("kaka", "kaka"), ("kiki", "kaka"), ("Hi! This is greate", "kiki"), ("kiki", "Hi! This is greate"),
        ("kaka+", "kiki"), ("kaka", "kiki+"), ("kaka-", "kiki"), ("kaka", "kiki-"), ("kaka-", "kiki+"),
        ("kaka\\-", "kiki"), ("k+-\\|-+$\\$aka", "kiki+"), (
            "ka=-=-00-43=-=-3=-=-=-=-=+_)+_489whgjh;lknf;gjkl;lks;glkf;lknaw4987098742p;ohasg=-=-=-=-+-+_+$_+$_+(*$_ka",
            "kiki",), ], )
def test_apply_string_delta(data_1, data_2):
    delta_steps = DeltaGenerator(data_1, data_2).generate_delta()

    delta = "".join([str(delta_step) for delta_step in delta_steps])
    assert DeltaApplier(delta).apply_string_delta(data_1) == data_2
    assert DeltaApplier(delta).apply_string_delta(data_2, reverse_delta=True) == data_1
