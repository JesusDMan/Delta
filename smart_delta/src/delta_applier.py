from smart_delta.src import UNMARK_MARK, INSERTION_MARK, REPLACEMENT_MARK, DELETION_MARK
from smart_delta.src.delta_element import parse_str_delta


class DeltaApplier:
    def __init__(self, delta_string):
        delta_steps = []
        indices = []
        is_after_mark = False

        for i in range(len(delta_string)):
            if delta_string[i] == UNMARK_MARK:
                if is_after_mark:
                    is_after_mark = False
                else:
                    is_after_mark = True
            if delta_string[i] != UNMARK_MARK and is_after_mark:
                is_after_mark = False

            elif (delta_string[i] == INSERTION_MARK or delta_string[i] == REPLACEMENT_MARK or delta_string[
                i] == DELETION_MARK) and not is_after_mark:
                indices.append(i)
        indices.append(len(delta_string))

        for i in range(len(indices) - 1):
            delta_steps.append(delta_string[indices[i]: indices[i + 1]])

        self.delta_elements = delta_steps

    def apply_string_delta(self, base_data, reverse_delta=False):
        delta_steps = self.delta_elements
        offset = 0
        data_with_delta = base_data
        for delta_step in delta_steps:
            delta_ = parse_str_delta(delta_step)
            data_with_delta, offset = delta_.apply_on_data(base_data=data_with_delta, apply_on_reverse=reverse_delta,
                                                           offset=offset)
        return data_with_delta

    def __str__(self):
        delta_string = ""
        for delta_step in self.delta_elements:
            delta_string += str(delta_step)
        return delta_string
