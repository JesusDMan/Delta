import pytest
from smart_delta.src.delta import *
from smart_delta.src.delta_utils import parse_str_delta, split_payload


@pytest.mark.parametrize(
    "delta_step_string, res",
    [
        ("+10|abc", ("+", 10, "abc")),
        ("-10|abc", ("-", 10, "abc")),
        ("%10|abc$def", ("%", 10, "abc", "def")),
        ("+10|a\\+bc", ("+", 10, "a+bc")),
        ("-10|a\\+bc", ("-", 10, "a+bc")),
        ("%10|a\\+bc$def", ("%", 10, "a+bc", "def")),
        ("+10|a\\-bc", ("+", 10, "a-bc")),
        ("-10|a\\-bc", ("-", 10, "a-bc")),
        ("%10|a\\-bc$def", ("%", 10, "a-bc", "def")),
        ("+10|a\\|bc", ("+", 10, "a|bc")),
        ("-10|a\\|bc", ("-", 10, "a|bc")),
        ("%10|a\\|bc$def", ("%", 10, "a|bc", "def")),
        ("+10|a\\$bc", ("+", 10, "a$bc")),
        ("-10|a\\$bc", ("-", 10, "a$bc")),
        ("%10|a\\$bc$def", ("%", 10, "a$bc", "def")),
        ("+10|a\\$bc", ("+", 10, "a$bc")),
    ],
)
def test_parse_str_delta(delta_step_string, res):
    if len(res) == 4:
        delta_res = Delta(res[0], res[1], res[2], res[3])
    else:
        delta_res = Delta(res[0], res[1], res[2])
    assert parse_str_delta(delta_step_string) == delta_res


@pytest.mark.parametrize(
    "payload,res",
    [
        ("abc$def", ("abc", "def")),
        ("a\\$bc$def", ("a\\$bc", "def")),
        ("abc$d\\$ef", ("abc", "d\\$ef")),
        ("abc\\$$def", ("abc\\$", "def")),
        ("abc$\\$def", ("abc", "\\$def")),
        ("\\$abc$def", ("\\$abc", "def")),
        ("abc$def\\$", ("abc", "def\\$")),
    ],
)
def test_split_payload(payload, res):
    assert split_payload(payload) == res
