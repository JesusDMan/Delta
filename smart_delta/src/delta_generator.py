from typing import Tuple, List, Optional, Union, Callable, Any, Iterable

from smart_delta.src import INSERTION_MARK, DELETION_MARK, REPLACEMENT_MARK, ENCODING
from smart_delta.src.delta_element import DeltaElement


class DeltaGenerator:
    DEFAULT_MAX_DIFF_LENGTH = 1000
    DEFAULT_MIN_LENGTH_FOR_FIT = 3

    def __init__(
        self,
        data_0: Union[str, bytes],
        data_1: Union[str, bytes],
        min_length_for_fit: Optional[int] = None,
        max_diff_length: Optional[int] = None,
    ):
        self.data_0 = data_0
        self.data_1 = data_1

        if type(self.data_0) is str:
            self.data_0 = bytes(self.data_0, encoding=ENCODING)
        if type(self.data_1) is str:
            self.data_1 = bytes(self.data_1, encoding=ENCODING)

        if min_length_for_fit:
            self.min_length_for_fit = min_length_for_fit
        else:
            self.min_length_for_fit = self.DEFAULT_MIN_LENGTH_FOR_FIT
        if max_diff_length:
            self.max_diff_length = max_diff_length
        else:
            self.max_diff_length = self.DEFAULT_MAX_DIFF_LENGTH

        self.delta_elements = self.generate_delta()

    def generate_delta(self) -> List[DeltaElement]:
        diff_beginning_index_0 = None
        delta_steps = []

        index_0, index_1 = 0, 0

        while index_0 < len(self.data_0) and index_1 < len(self.data_1):
            if self.data_0[index_0] != self.data_1[index_1]:
                diff_beginning_index_0 = index_0
                diff_beginning_index_1 = index_1
                diff_ending_0, diff_ending_1 = self.range_diff(
                    self.data_0[diff_beginning_index_0:],
                    self.data_1[diff_beginning_index_1:],
                )
                diff_ending_0 += diff_beginning_index_0
                diff_ending_1 += diff_beginning_index_1

                if (
                    diff_ending_0 != diff_beginning_index_0
                    and diff_ending_1 == diff_beginning_index_1
                ):
                    delta_steps.append(
                        DeltaElement(
                            DELETION_MARK,
                            diff_beginning_index_1,
                            self.data_0[diff_beginning_index_0:diff_ending_0],
                        )
                    )

                elif (
                    diff_ending_1 != diff_beginning_index_1
                    and diff_ending_0 == diff_beginning_index_0
                ):
                    delta_steps.append(
                        DeltaElement(
                            INSERTION_MARK,
                            diff_beginning_index_1,
                            self.data_1[diff_beginning_index_1:diff_ending_1],
                        )
                    )

                elif (
                    diff_ending_0 != diff_beginning_index_0
                    and diff_ending_1 != diff_beginning_index_1
                ):
                    delta_steps.append(
                        DeltaElement(
                            REPLACEMENT_MARK,
                            diff_beginning_index_1,
                            self.data_0[diff_beginning_index_0:diff_ending_0],
                            self.data_1[diff_beginning_index_1:diff_ending_1],
                        )
                    )

                index_0 = diff_ending_0 - 1
                index_1 = diff_ending_1 - 1

                diff_beginning_index_0 = None

            index_0 += 1
            index_1 += 1

        if not diff_beginning_index_0:
            diff_beginning_index_0 = index_0
            diff_beginning_index_1 = index_1

        if index_0 < len(self.data_0) and index_1 >= len(self.data_1):
            delta_steps.append(
                DeltaElement(
                    DELETION_MARK,
                    diff_beginning_index_1,
                    self.data_0[diff_beginning_index_0:],
                )
            )

        if index_1 < len(self.data_1) and index_0 >= len(self.data_0):
            delta_steps.append(
                DeltaElement(
                    INSERTION_MARK,
                    diff_beginning_index_1,
                    self.data_1[diff_beginning_index_1:],
                )
            )
        return delta_steps

    def range_diff(self, data_0: bytes, data_1: bytes) -> Tuple[int, int]:
        index_0_for_0, index_1_for_0 = 0, 0
        index_0_for_1, index_1_for_1 = 0, 0

        check_index_in_range: Callable[
            [int, bytes], bool
        ] = lambda index, data: index < self.max_diff_length and index < len(data)

        slice_data: Callable[[bytes, int, int], bytes] = lambda l, b: l[
            b : b + self.min_length_for_fit
        ]

        while index_0_for_0 < len(data_0) and index_1_for_1 < len(data_1):
            while True:
                if not check_index_in_range(
                    index_1_for_0, data_1
                ) and not check_index_in_range(index_0_for_1, data_0):
                    break

                if slice_data(data_0, index_0_for_0) == slice_data(
                    data_1, index_1_for_0
                ):
                    return index_0_for_0, index_1_for_0

                if slice_data(data_1, index_1_for_1) == slice_data(
                    data_0, index_0_for_1
                ):
                    return index_0_for_1, index_1_for_1

                index_1_for_0 += 1
                index_0_for_1 += 1

            index_0_for_0 += 1
            index_1_for_0 = 0
            index_0_for_1 = 0
            index_1_for_1 += 1
        return len(data_0), len(data_1)

    def __bytes__(self):
        delta_string = b""
        for delta_step in self.delta_elements:
            delta_string += bytes(delta_step)
        return delta_string

    def __str__(self):
        return bytes(self).decode(ENCODING)


def range_fit(data_0, data_1) -> int:
    min_len = min(len(data_0), len(data_1))
    for index in range(min_len):
        if data_0[index] != data_1[index]:
            return index
    return min_len
