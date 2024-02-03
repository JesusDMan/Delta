import pytest

from smart_delta.src.delta_generator import DeltaGenerator


@pytest.mark.parametrize("data_0,data_1,res",
    [("Hi! Duck", "Hi! Duck", []), ("Hi! lala Duck Gargamel", "Hi! Duck", ["-4|lala ", "-8| Gargamel"]),
        ("Hi! Duck", "Hi! lili Duck", ["+4|lili "]), ("Hi! lala Duck", "Hi! ronron Duck", ["%4|lala$ronron"]),
        ("Hi! lala Duck Gargamel", "Hi! Duck shish gon", ["-4|lala ", "%9|Gargamel$shish gon"],),
        ("Hi! \\+-|%$ Duck", "Hi! Duck", ["-4|\\\\\\+\\-\\|\\%\\$ "]),
        ("Hi! Duck", "Hi! \\+-|%$ Duck", ["+4|\\\\\\+\\-\\|\\%\\$ "]),
        ("Hi! Duck", "Hi!f fDuckf f", ["%3| $f f", "+10|f f"]),
        ("Hello! My name is John Cena. %, + and - are signs used for parsing the delta. "
         "In addition, there's | and $. \\ is used to mark usage of safe signs in the text.",
         "Hello! My name is Jeff Bazos. There are signs used for parsing the delta, such as +, % and -. "
         "There's also $ and |. To mark usage of safe signs in the text, we use \\.",
         ["%19|ohn Cena. \\%, \\+ and \\-$eff Bazos. There", "%72|. In addition, t$, such as \\+, \\% and \\-. T",
             "%102|\\|$also \\$", "%113|\\$. \\\\ is$\\|. To mark", "%126|ed to mark$age of safe signs in the text, we",
             "%162|age of safe signs in the text$e \\\\", ],), ], )
def test_generate_delta(data_0, data_1, res):
    delta_steps = DeltaGenerator(data_0, data_1).delta_elements

    delta_steps = [str(delta_step) for delta_step in delta_steps]
    assert delta_steps == res
