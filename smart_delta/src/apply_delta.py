from smart_delta.src import delta, INSERTION_MARK, REPLACEMENT_MARK, DELETION_MARK
from smart_delta.src.delta_utils import *


def parse_delta_steps(delta_string):
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

        elif ((delta_string[i] == INSERTION_MARK or
              delta_string[i] == REPLACEMENT_MARK or
              delta_string[i] == DELETION_MARK) and
              not is_after_mark):
            indices.append(i)
    indices.append(len(delta_string))

    for i in range(len(indices) - 1):
        delta_steps.append(delta_string[indices[i]:indices[i + 1]])
    return delta_steps


def apply_delta_step(base_data: str, delta, reverse_delta=False, offset=0):
    data_with_delta = base_data
    sign = delta.sign
    index = delta.index
    delta_payload = delta.payload

    if reverse_delta:
        if sign == DELETION_MARK:
            data_with_delta = base_data[0:index + offset] + delta_payload + base_data[index + offset:]
            offset += len(delta_payload)
        if sign == INSERTION_MARK:
            data_with_delta = base_data[0:index + offset] + base_data[index + len(delta_payload) + offset:]
            offset -= len(delta_payload)
        if sign == REPLACEMENT_MARK:
            data_with_delta = base_data[0:index + offset] + delta_payload + base_data[
                                                                            index + len(delta.second_payload) + offset:]
            offset += len(delta_payload) - len(delta.second_payload)

    else:
        if sign == DELETION_MARK:
            data_with_delta = base_data[0:index] + base_data[index + len(delta_payload):]
        if sign == INSERTION_MARK:
            data_with_delta = base_data[0:index] + delta_payload + base_data[index:]
        if sign == REPLACEMENT_MARK:
            data_with_delta = base_data[0:index] + delta.second_payload + base_data[index + len(delta_payload):]

    return data_with_delta, offset


def apply_string_delta(base_data, delta_string, reverse_delta=False):
    delta_steps = parse_delta_steps(delta_string)
    offset = 0
    data_with_delta = base_data
    for delta_step in delta_steps:
        delta_ = delta.parse_str_delta(delta_step)
        data_with_delta, offset = apply_delta_step(base_data=data_with_delta,
                                                   delta=delta_, reverse_delta=reverse_delta,
                                                   offset=offset)
    return data_with_delta
