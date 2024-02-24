import time
from typing import Tuple, List, Optional

from smart_delta.src import (INSERTION_MARK, DELETION_MARK, REPLACEMENT_MARK, )
from smart_delta.src.delta_element import DeltaElement


class DeltaGenerator:
    DEFAULT_MAX_DIFF_LENGTH = 1000
    DEFAULT_MIN_LENGTH_FOR_FIT = 3

    def __init__(
            self,
            data_0,
            data_1,
            min_length_for_fit: Optional[int] = None,
            max_diff_length: Optional[int] = None
    ):
        self.data_0 = data_0
        self.data_1 = data_1
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
                diff_ending_0, diff_ending_1 = self.range_diff(self.data_0[diff_beginning_index_0:],
                                                               self.data_1[diff_beginning_index_1:])
                diff_ending_0 += diff_beginning_index_0
                diff_ending_1 += diff_beginning_index_1

                if (diff_ending_0 != diff_beginning_index_0 and diff_ending_1 == diff_beginning_index_1):
                    delta_steps.append(DeltaElement(DELETION_MARK, diff_beginning_index_1,
                                                    self.data_0[diff_beginning_index_0:diff_ending_0], ))

                elif (diff_ending_1 != diff_beginning_index_1 and diff_ending_0 == diff_beginning_index_0):
                    delta_steps.append(DeltaElement(INSERTION_MARK, diff_beginning_index_1,
                                                    self.data_1[diff_beginning_index_1:diff_ending_1], ))

                elif (diff_ending_0 != diff_beginning_index_0 and diff_ending_1 != diff_beginning_index_1):
                    delta_steps.append(DeltaElement(REPLACEMENT_MARK, diff_beginning_index_1,
                                                    self.data_0[diff_beginning_index_0:diff_ending_0],
                                                    self.data_1[diff_beginning_index_1:diff_ending_1], ))

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
                DeltaElement(DELETION_MARK, diff_beginning_index_1, self.data_0[diff_beginning_index_0:]))

        if index_1 < len(self.data_1) and index_0 >= len(self.data_0):
            delta_steps.append(
                DeltaElement(INSERTION_MARK, diff_beginning_index_1, self.data_1[diff_beginning_index_1:]))

        return delta_steps

    # def search_fit(self, data_0, data_1, index_0, index_1):

    def range_diff(self, data_0: str, data_1: str) -> Tuple[int, int]:
        fit_index_0, fit_index_1 = len(data_0), len(data_1)
        index_0_for_0, index_1_for_0 = 0, 0
        index_0_for_1, index_1_for_1 = 0, 0
        res = False

        while not res:
            while True:
                if index_0_for_0 >= len(data_0) and index_1_for_1:
                    res = True
                    break
                if index_0_for_0 >= len(data_0) and index_1_for_1 >= len(data_1) or (not (index_1_for_0 < self.max_diff_length and index_1_for_0 <= len(data_1)) and not (index_0_for_1 < self.max_diff_length and index_0_for_1 <= len(data_0))):
                    # input()
                    break

                # print("==============\nData_0 for 0: ", data_0[index_0_for_0: index_0_for_0 + self.min_length_for_fit])
                # print("Data_1 for 0: ", data_1[index_1_for_0: index_1_for_0 + self.min_length_for_fit])
                # print("Data_1 for 1: ", data_1[index_1_for_1: index_1_for_1 + self.min_length_for_fit])
                # print("Data_0 for 1: ", data_0[index_0_for_1: index_0_for_1 + self.min_length_for_fit])
                # print(f"{index_0_for_0=} , {index_1_for_0=} | {index_0_for_1=}, {index_1_for_1=}")
                # print("==============\n")
                # time.sleep(0.01)

                if index_1_for_0 < self.max_diff_length and index_1_for_0 <= len(data_1):
                    if (
                            data_0[index_0_for_0: index_0_for_0 + self.min_length_for_fit] ==
                            data_1[index_1_for_0: index_1_for_0 + self.min_length_for_fit]
                    ):
                        fit_index_0 = index_0_for_0
                        fit_index_1 = index_1_for_0
                        res = True
                        break
                    else:
                        index_1_for_0 += 1


                if index_0_for_1 < self.max_diff_length and index_0_for_1 <= len(data_0):
                    if (
                            data_1[index_1_for_1: index_1_for_1 + self.min_length_for_fit] ==
                            data_0[index_0_for_1: index_0_for_1 + self.min_length_for_fit]
                    ):
                        fit_index_0 = index_0_for_1
                        fit_index_1 = index_1_for_1
                        res = True
                        break
                    else:
                        index_0_for_1 += 1

            index_0_for_0 += 1
            index_1_for_0 = 0
            index_0_for_1 = 0
            index_1_for_1 += 1
            # input()
        return fit_index_0, fit_index_1

    def __str__(self):
        delta_string = ""
        for delta_step in self.delta_elements:
            delta_string += str(delta_step)
        return delta_string
