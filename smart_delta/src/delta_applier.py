from smart_delta.src import INSERTION_MARK, REPLACEMENT_MARK, DELETION_MARK
from smart_delta.src.delta_element import parse_str_delta_element
from smart_delta.src.delta_utils import find_system_marks


class DeltaApplier:
    def __init__(self, delta_string: str):
        self.delta_elements = []
        indices = find_system_marks(delta_string, (INSERTION_MARK, REPLACEMENT_MARK, DELETION_MARK))
        indices.append(len(delta_string))

        for i in range(len(indices) - 1):
            self.delta_elements.append(delta_string[indices[i]: indices[i + 1]])

    def apply_on_data(self, base_data: str, reverse_delta: bool = False) -> str:
        delta_steps = self.delta_elements
        offset = 0
        data_with_delta = base_data
        for delta_step in delta_steps:
            delta_ = parse_str_delta_element(delta_step)
            data_with_delta, offset = delta_.apply_on_data(base_data=data_with_delta, apply_on_reverse=reverse_delta,
                                                           offset=offset)
        return data_with_delta

    def __str__(self) -> str:
        delta_string = ""
        for delta_step in self.delta_elements:
            delta_string += str(delta_step)
        return delta_string
