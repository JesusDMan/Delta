from typing import List, Optional

import pytest

from smart_delta.src.delta_generator import DeltaGenerator


@pytest.mark.parametrize("data_0,data_1,max_diff_length, min_length_for_fit,res",
                         [("Hi! Duck", "Hi! Duck", None, None, []),
                          ("Hi! lala Duck Gargamel", "Hi! Duck", None, None, ["-4|lala ", "-8| Gargamel"]),
                          ("Hi! Duck", "Hi! lili Duck", None, None, ["+4|lili "]),
                          ("Hi! lala Duck", "Hi! ronron Duck", None, None, ["%4|lala$ronron"]),
                          ("Hi! lala Duck Gargamel", "Hi! Duck shish gon", None, None,
                           ["-4|lala ", "%9|Gargamel$shish gon"],),
                          ("Hi! \\+-|%$ Duck", "Hi! Duck", None, None, ["-4|\\\\\\+\\-\\|\\%\\$ "]),
                          ("Hi! Duck", "Hi! \\+-|%$ Duck", None, None, ["+4|\\\\\\+\\-\\|\\%\\$ "]),
                          ("Hi! Duck", "Hi!f fDuckf f", None, None, ["%3| $f f", "+10|f f"]),
                          ("Hello! My name is John Cena. %, + and - are signs used for parsing the delta. "
                           "In addition, there's | and $. \\ is used to mark usage of safe signs in the text.",
                           "Hello! My name is Jeff Bazos. There are signs used for parsing the delta, such as +, % and -. "
                           "There's also $ and |. To mark usage of safe signs in the text, we use \\.", 50, 3,
                           ["%19|ohn Cena. \\%, \\+ and \\- a$eff Bazos. The", "+36|are ",
                            "%72|. In addition, there's \\|$, such as \\+, \\%",
                            "%91|\\$. \\\\ is$\\-. There's also \\$ and \\|. To mark", "-126|ed to mark us",
                            "+155|, we use \\\\"]
                           ,),
                          ],

                         )
def test_generate_delta(data_0: str, data_1: str, max_diff_length: Optional[int],
                        min_length_for_fit: Optional[int],
                        res: List[str]):
    print(data_0)
    print(data_1)
    # print(res)
    delta_steps = DeltaGenerator(
        data_0,
        data_1,
        max_diff_length=max_diff_length,
        min_length_for_fit=min_length_for_fit
    ).delta_elements
    print(delta_steps)
    delta_steps = [str(delta_step) for delta_step in delta_steps]
    assert delta_steps == res
