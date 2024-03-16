from typing import Optional, Tuple

import pytest

from smart_delta.src.delta_element import DeltaElement


@pytest.mark.parametrize(
    "base_data,delta_element_parameters,data_with_delta",
    [
        (b"Hi| Duck", (b"%", 2, b"|", b"!"), b"Hi! Duck"),
        (b"Hi! Duck", (b"%", 2, b"!", b"|"), b"Hi| Duck"),
        (b"Hi! Duck", (b"+", 8, b"er"), b"Hi! Ducker"),
        (b"Hi! Ducker", (b"-", 8, b"er"), b"Hi! Duck"),
        (b"Hi! I'm a Duck", (b"-", 4, b"I'm a "), b"Hi! Duck"),
        (b"Hi! Duck", (b"+", 4, b"I'm a "), b"Hi! I'm a Duck"),
        (b"Hi! This is a Duck", (b"%", 4, b"This is", b"I'm"), b"Hi! I'm a Duck"),
        (b"Hi! Duck", (b"+", 4, b"+-|$% "), b"Hi! +-|$% Duck"),
        (b"Hi! +-|$% Duck", (b"%", 4, b"+-|$%", b"|%$-+"), b"Hi! |%$-+ Duck"),
    ],
)
def test_data_element_is_applied_correctly(
    base_data: bytes,
    delta_element_parameters: Tuple[bytes, int, bytes, Optional[bytes]],
    data_with_delta: bytes,
):
    delta_element = DeltaElement(*delta_element_parameters)
    assert delta_element.apply_on_data(base_data=base_data)[0] == data_with_delta
    assert (
        delta_element.apply_on_data(base_data=data_with_delta, apply_on_reverse=True)[0]
        == base_data
    )
