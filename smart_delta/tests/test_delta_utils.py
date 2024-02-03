from typing import Tuple

import pytest

from smart_delta.src.delta_utils import split_payload


@pytest.mark.parametrize("payload,res",
                         [("abc$def", ("abc", "def")), ("a\\$bc$def", ("a\\$bc", "def")),
                          ("abc$d\\$ef", ("abc", "d\\$ef")),
                          ("abc\\$$def", ("abc\\$", "def")), ("abc$\\$def", ("abc", "\\$def")),
                          ("\\$abc$def", ("\\$abc", "def")),
                          ("abc$def\\$", ("abc", "def\\$")), ], )
def test_split_payload(payload: str, res: Tuple[str, str]):
    assert split_payload(payload) == res
