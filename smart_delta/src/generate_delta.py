from typing import List, Optional

from smart_delta.src import apply_delta, delta_utils, INSERTION_MARK, DELETION_MARK, REPLACEMENT_MARK, \
    INDEX_PAYLOAD_SEPERATOR_MARK, REPLACEMENT_SPLIT_MARK, SAFE_MARKS, REGULAR_MARKS, UNMARK_MARK
from smart_delta.src.apply_delta import parse_delta_steps
from smart_delta.src.delta_utils import replace_signs


def range_diff(data_0, data_1):
    length_for_fitting = 3
    length_for_diff = 50
    fit_index_0, fit_index_1 = len(data_0), len(data_1)
    index_0_for_0, index_1_for_0 = 0, 0
    res = False
    while not res and index_0_for_0 <= len(data_0):
        while index_1_for_0 < length_for_diff and index_1_for_0 <= len(data_1):
            if data_0[index_0_for_0:index_0_for_0 + length_for_fitting] == data_1[
                                                                           index_1_for_0:index_1_for_0 + length_for_fitting]:
                fit_index_0 = index_0_for_0
                fit_index_1 = index_1_for_0
                res = True
                break
            else:
                index_1_for_0 += 1
        index_0_for_0 += 1
        index_1_for_0 = 0
    return fit_index_0, fit_index_1


def create_delta_step(sign, index, payload, second_payload: Optional[str] = None):
    for possible_sign in ["\\"] + REGULAR_MARKS:
        payload = replace_signs(payload, possible_sign, UNMARK_MARK + possible_sign)
        if second_payload:
            second_payload = second_payload.replace(possible_sign, UNMARK_MARK + possible_sign)
    if second_payload:
        payload = f"{payload}{REPLACEMENT_SPLIT_MARK}{second_payload}"
    return f"{sign}{index}{INDEX_PAYLOAD_SEPERATOR_MARK}{payload}"


def create_delta_steps_list(data_0, data_1):
    diff_beginning_index_0 = None
    res = []

    index_0, index_1 = 0, 0

    while index_0 < len(data_0) and index_1 < len(data_1):
        if data_0[index_0] != data_1[index_1]:
            diff_beginning_index_0 = index_0
            diff_beginning_index_1 = index_1
            diff_ending_0, diff_ending_1 = range_diff(data_0[diff_beginning_index_0:], data_1[diff_beginning_index_1:])
            diff_ending_0 += diff_beginning_index_0
            diff_ending_1 += diff_beginning_index_1

            if diff_ending_0 != diff_beginning_index_0 and diff_ending_1 == diff_beginning_index_1:
                res.append(create_delta_step(DELETION_MARK, diff_beginning_index_1, data_0[diff_beginning_index_0:diff_ending_0]))

            elif diff_ending_1 != diff_beginning_index_1 and diff_ending_0 == diff_beginning_index_0:
                res.append(create_delta_step(INSERTION_MARK, diff_beginning_index_1, data_1[diff_beginning_index_1:diff_ending_1]))

            elif diff_ending_0 != diff_beginning_index_0 and diff_ending_1 != diff_beginning_index_1:
                res.append(create_delta_step(REPLACEMENT_MARK, diff_beginning_index_1, data_0[diff_beginning_index_0:diff_ending_0],
                                             data_1[diff_beginning_index_1:diff_ending_1]))

            index_0 = diff_ending_0 - 1
            index_1 = diff_ending_1 - 1

            diff_beginning_index_0 = None

        index_0 += 1
        index_1 += 1

    if not diff_beginning_index_0:
        diff_beginning_index_0 = index_0
        diff_beginning_index_1 = index_1

    if index_0 < len(data_0) and index_1 >= len(data_1):
        res.append(create_delta_step(DELETION_MARK, diff_beginning_index_1, data_0[diff_beginning_index_0:]))

    if index_1 < len(data_1) and index_0 >= len(data_0):
        res.append(create_delta_step(INSERTION_MARK, diff_beginning_index_1, data_1[diff_beginning_index_1:]))

    return res


def create_delta_string(delta_steps: List[str]):
    delta_string = ""
    for delta_step in delta_steps:
        delta_string += delta_step
    return delta_string


def main():
    data_1 = "Hello! My name is John Cena. %, + and - are signs used for parsing the delta. " \
             "In addition, there's | and $. \\ is used to mark usage of safe signs in the text."
    data_2 = "Hello! My name is Jeff Bazos. There are signs used for parsing the delta, such as +, % and -. " \
             "There's also $ and |. To mark usage of safe signs in the text, we use \\."

    delta_utils.print_data(data_1)
    print()
    delta_utils.print_data(data_2)
    print()
    delta_list = create_delta_steps_list(data_1, data_2)
    delta = create_delta_string(delta_list)
    print(delta_list)
    print(repr(delta))

    print(parse_delta_steps(delta))
    print(apply_delta.apply_string_delta(data_1, delta))
    print(data_2)
    print("-"*99)
    print(apply_delta.apply_string_delta(data_2, delta, reverse_delta=True))
    print(data_1)


if __name__ == '__main__':
    main()