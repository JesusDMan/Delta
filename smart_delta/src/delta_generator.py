from smart_delta.src import (INSERTION_MARK, DELETION_MARK, REPLACEMENT_MARK, )
from smart_delta.src.delta_element import DeltaElement


class DeltaGenerator:
    def __init__(self, data_0, data_1):
        self.data_0 = data_0
        self.data_1 = data_1
        self.length_for_fitting = 3
        self.max_diff_length = 50
        self.delta_elements = self.generate_delta()

    def generate_delta(self):
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

    def range_diff(self, data_0, data_1):
        fit_index_0, fit_index_1 = len(data_0), len(data_1)
        index_0_for_0, index_1_for_0 = 0, 0
        res = False
        while not res and index_0_for_0 <= len(data_0):
            while index_1_for_0 < self.max_diff_length and index_1_for_0 <= len(data_1):
                if (data_0[index_0_for_0: index_0_for_0 + self.length_for_fitting] == data_1[
                                                                                      index_1_for_0: index_1_for_0 + self.length_for_fitting]):
                    fit_index_0 = index_0_for_0
                    fit_index_1 = index_1_for_0
                    res = True
                    break
                else:
                    index_1_for_0 += 1
            index_0_for_0 += 1
            index_1_for_0 = 0
        return fit_index_0, fit_index_1

    def __str__(self):
        delta_string = ""
        for delta_step in self.delta_elements:
            delta_string += str(delta_step)
        return delta_string
