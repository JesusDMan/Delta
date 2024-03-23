from typing import Tuple

import pytest

from smart_delta.src.delta_utils import split_payload, range_diff


@pytest.mark.parametrize(
    "payload,res",
    [
        (b"abc$def", (b"abc", b"def")),
        (b"a\\$bc$def", (b"a\\$bc", b"def")),
        (b"abc$d\\$ef", (b"abc", b"d\\$ef")),
        (b"abc\\$$def", (b"abc\\$", b"def")),
        (b"abc$\\$def", (b"abc", b"\\$def")),
        (b"\\$abc$def", (b"\\$abc", b"def")),
        (b"abc$def\\$", (b"abc", b"def\\$")),
    ],
)
def test_split_payload(payload: str, res: Tuple[str, str]):
    assert split_payload(payload) == res


@pytest.mark.parametrize(
    "data_0,data_1,max_diff_length,min_length_for_fit,true_res",
    [
        (b"123456", b"123456", 3, 3, (0, 0)),
        (b"123456", b"323456", 3, 3, (1, 1)),
        (b"123456", b"3123456", 3, 3, (0, 1)),
        (b"3123456", b"123456", 3, 3, (1, 0)),
        (b"123456", b"111111", 3, 3, (6, 6)),
        (b"123456", b"1111111", 3, 3, (6, 7)),
        (b"1234567", b"111111", 3, 3, (7, 6)),
    ],
)
def test_range_diff(
    data_0: bytes,
    data_1: bytes,
    max_diff_length,
    min_length_for_fit,
    true_res: Tuple[int, int],
):
    res = range_diff(
        data_0,
        data_1,
        max_diff_length=max_diff_length,
        min_length_for_fit=min_length_for_fit,
    )
    assert res == true_res
