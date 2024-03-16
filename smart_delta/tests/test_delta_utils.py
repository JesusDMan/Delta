from typing import Tuple

import pytest

from smart_delta.src.delta_utils import split_payload


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
