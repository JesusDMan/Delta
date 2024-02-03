import pytest

from smart_delta.src.delta_element import DeltaElement


@pytest.mark.parametrize("base_data,delta_element_parameters,data_with_delta",
                         [("Hi| Duck", ("%", 2, "|", "!"), "Hi! Duck"), ("Hi! Duck", ("%", 2, "!", "|"), "Hi| Duck"),
                          ("Hi! Duck", ("+", 8, "er"), "Hi! Ducker"), ("Hi! Ducker", ("-", 8, "er"), "Hi! Duck"),
                          ("Hi! I'm a Duck", ("-", 4, "I'm a "), "Hi! Duck"),
                          ("Hi! Duck", ("+", 4, "I'm a "), "Hi! I'm a Duck"),
                          ("Hi! This is a Duck", ("%", 4, "This is", "I'm"), "Hi! I'm a Duck"),
                          ("Hi! Duck", ("+", 4, "+-|$% "), "Hi! +-|$% Duck"),
                          ("Hi! +-|$% Duck", ("%", 4, "+-|$%", "|%$-+"), "Hi! |%$-+ Duck"), ], )
def test_data_element_is_applied_correctly(base_data, delta_element_parameters, data_with_delta):
    delta_element = DeltaElement(*delta_element_parameters)
    assert delta_element.apply_on_data(base_data=base_data)[0] == data_with_delta
    assert (delta_element.apply_on_data(base_data=data_with_delta, apply_on_reverse=True)[0] == base_data)
