from typing import Optional, Tuple, List

import pytest

from smart_delta.src.delta_applier import DeltaApplier
from smart_delta.src.delta_element import parse_str_delta_element, DeltaElement


@pytest.mark.parametrize("delta_element_string, true_delta_element_parameters",
                         [("+10|abc", ("+", 10, "abc")), ("-10|abc", ("-", 10, "abc")),
                          ("%10|abc$def", ("%", 10, "abc", "def")),
                          ("+10|a\\+bc", ("+", 10, "a+bc")), ("-10|a\\+bc", ("-", 10, "a+bc")),
                          ("%10|a\\+bc$def", ("%", 10, "a+bc", "def")), ("+10|a\\-bc", ("+", 10, "a-bc")),
                          ("-10|a\\-bc", ("-", 10, "a-bc")), ("%10|a\\-bc$def", ("%", 10, "a-bc", "def")),
                          ("+10|a\\|bc", ("+", 10, "a|bc")), ("-10|a\\|bc", ("-", 10, "a|bc")),
                          ("%10|a\\|bc$def", ("%", 10, "a|bc", "def")), ("+10|a\\$bc", ("+", 10, "a$bc")),
                          ("-10|a\\$bc", ("-", 10, "a$bc")), ("%10|a\\$bc$def", ("%", 10, "a$bc", "def")),
                          ("+10|a\\$bc", ("+", 10, "a$bc")), ], )
def test_parse_str_delta_element(delta_element_string: str, true_delta_element_parameters: Tuple[str, int, str, Optional[str]]):
    delta_res = DeltaElement(*true_delta_element_parameters)
    assert parse_str_delta_element(delta_element_string) == delta_res


@pytest.mark.parametrize("delta_string,parsed_delta_steps",
                         [("+1|lala", ["+1|lala"]), ("-1|lala", ["-1|lala"]), ("%1|lala$lili", ["%1|lala$lili"]),
                          ("+1|lala+4|lili", ["+1|lala", "+4|lili"]),
                          ("+1|lala\\\\+4|lili", ["+1|lala\\\\", "+4|lili"]),
                          ("-1|lala-4|lili", ["-1|lala", "-4|lili"]),
                          ("%1|lala$lili%4|lili$lala", ["%1|lala$lili", "%4|lili$lala"]), (
                                  "%6|dd my\\$\\-=\\$\\$\\|\\|=\\-\\\\\\$\\+\\|\\| n\\+$my n%18|\\-$\\+_\\+_\\$\\+_\\+=\\-=\\-=\\-=%39|ce\\\\na  this is yayyyy$ron goron",
                                  ["%6|dd my\\$\\-=\\$\\$\\|\\|=\\-\\\\\\$\\+\\|\\| n\\+$my n",
                                   "%18|\\-$\\+_\\+_\\$\\+_\\+=\\-=\\-=\\-=",
                                   "%39|ce\\\\na  this is yayyyy$ron goron", ],), ], )
def test_delta_applier_parses_delta_string_correctly(delta_string: str, parsed_delta_steps: List[str]):
    assert DeltaApplier(delta_string).delta_elements == parsed_delta_steps
