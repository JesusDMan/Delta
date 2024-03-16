from typing import Optional, Tuple, List

import pytest

from smart_delta.src.delta_applier import DeltaApplier
from smart_delta.src.delta_element import parse_str_delta_element, DeltaElement


@pytest.mark.parametrize(
    "delta_element_string, true_delta_element_parameters",
    [
        (b"+10|abc", (b"+", 10, b"abc")),
        (b"-10|abc", (b"-", 10, b"abc")),
        (b"%10|abc$def", (b"%", 10, b"abc", b"def")),
        (b"+10|a\\+bc", (b"+", 10, b"a+bc")),
        (b"-10|a\\+bc", (b"-", 10, b"a+bc")),
        (b"%10|a\\+bc$def", (b"%", 10, b"a+bc", b"def")),
        (b"+10|a\\-bc", (b"+", 10, b"a-bc")),
        (b"-10|a\\-bc", (b"-", 10, b"a-bc")),
        (b"%10|a\\-bc$def", (b"%", 10, b"a-bc", b"def")),
        (b"+10|a\\|bc", (b"+", 10, b"a|bc")),
        (b"-10|a\\|bc", (b"-", 10, b"a|bc")),
        (b"%10|a\\|bc$def", (b"%", 10, b"a|bc", b"def")),
        (b"+10|a\\$bc", (b"+", 10, b"a$bc")),
        (b"-10|a\\$bc", (b"-", 10, b"a$bc")),
        (b"%10|a\\$bc$def", (b"%", 10, b"a$bc", b"def")),
        (b"+10|a\\$bc", (b"+", 10, b"a$bc")),
    ],
)
def test_parse_str_delta_element(
    delta_element_string: bytes,
    true_delta_element_parameters: Tuple[bytes, int, bytes, Optional[bytes]],
):
    delta_res = DeltaElement(*true_delta_element_parameters)
    assert parse_str_delta_element(delta_element_string) == delta_res


@pytest.mark.parametrize(
    "delta_bytes_string,parsed_delta_steps",
    [
        (b"+1|lala", [b"+1|lala"]),
        (b"-1|lala", [b"-1|lala"]),
        (b"%1|lala$lili", [b"%1|lala$lili"]),
        (b"+1|lala+4|lili", [b"+1|lala", b"+4|lili"]),
        (b"+1|lala\\\\+4|lili", [b"+1|lala\\\\", b"+4|lili"]),
        (b"-1|lala-4|lili", [b"-1|lala", b"-4|lili"]),
        (b"%1|lala$lili%4|lili$lala", [b"%1|lala$lili", b"%4|lili$lala"]),
        (
            b"%6|dd my\\$\\-=\\$\\$\\|\\|=\\-\\\\\\$\\+\\|\\| n\\+$my n%18|\\-$\\+_\\+_\\$\\+_\\+=\\-=\\-=\\-=%39|ce\\\\na  this is yayyyy$ron goron",
            [
                b"%6|dd my\\$\\-=\\$\\$\\|\\|=\\-\\\\\\$\\+\\|\\| n\\+$my n",
                b"%18|\\-$\\+_\\+_\\$\\+_\\+=\\-=\\-=\\-=",
                b"%39|ce\\\\na  this is yayyyy$ron goron",
            ],
        ),
    ],
)
def test_delta_applier_parses_delta_string_correctly(
    delta_bytes_string: bytes, parsed_delta_steps: List[bytes]
):
    parsed_delta_elements_bytes = parsed_delta_steps
    assert (
        DeltaApplier(delta_bytes_string).delta_elements_bytes
        == parsed_delta_elements_bytes
    )
