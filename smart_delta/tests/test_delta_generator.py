from typing import List, Optional

import pytest

from smart_delta.src.delta_generator import DeltaGenerator


@pytest.mark.parametrize(
    "data_0,data_1,max_diff_length, min_length_for_fit,res",
    [
        (b"Hi! Duck", b"Hi! Duck", None, None, []),
        (
            b"Hi! lala Duck Gargamel",
            b"Hi! Duck",
            None,
            None,
            [b"-4|lala ", b"-8| Gargamel"],
        ),
        (b"Hi! Duck", b"Hi! lili Duck", None, None, [b"+4|lili "]),
        (b"Hi! lala Duck", b"Hi! ronron Duck", None, None, [b"%4|lala$ronron"]),
        (
            b"Hi! lala Duck Gargamel",
            b"Hi! Duck shish gon",
            None,
            None,
            [b"-4|lala ", b"%9|Gargamel$shish gon"],
        ),
        (b"Hi! \\+-|%$ Duck", b"Hi! Duck", None, None, [b"-4|\\\\\\+\\-\\|\\%\\$ "]),
        (b"Hi! Duck", b"Hi! \\+-|%$ Duck", None, None, [b"+4|\\\\\\+\\-\\|\\%\\$ "]),
        (b"Hi! Duck", b"Hi!f fDuckf f", None, None, [b"%3| $f f", b"+10|f f"]),
        (
            b"Hello! My name is John Cena. %, + and - are signs used for parsing the delta. "
            b"In addition, there's | and $. \\ is used to mark usage of safe signs in the text.",
            b"Hello! My name is Jeff Bazos. There are signs used for parsing the delta, such as +, % and -. "
            b"There's also $ and |. To mark usage of safe signs in the text, we use \\.",
            50,
            3,
            [
                b"%19|ohn Cena. \\%, \\+ and \\- a$eff Bazos. The",
                b"+36|are ",
                b"%72|. In addition, there's \\|$, such as \\+, \\%",
                b"%91|\\$. \\\\ is$\\-. There's also \\$ and \\|. To mark",
                b"-126|ed to mark us",
                b"+155|, we use \\\\",
            ],
        ),
    ],
)
def test_generate_delta(
    data_0: bytes,
    data_1: bytes,
    max_diff_length: Optional[int],
    min_length_for_fit: Optional[int],
    res: List[bytes],
):
    delta_steps = DeltaGenerator(
        data_0,
        data_1,
        max_diff_length=max_diff_length,
        min_length_for_fit=min_length_for_fit,
    ).delta_elements
    print(delta_steps)
    delta_steps = [bytes(delta_step) for delta_step in delta_steps]
    assert delta_steps == res
