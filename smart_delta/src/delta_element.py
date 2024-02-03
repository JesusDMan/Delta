from typing import Optional

from smart_delta.src import REPLACEMENT_MARK, REPLACEMENT_SPLIT_MARK, INDEX_PAYLOAD_SEPERATOR_MARK, UNMARK_MARK, \
    REGULAR_MARKS, DELETION_MARK, INSERTION_MARK
from smart_delta.src.delta_utils import replace_signs, split_payload


class DeltaElement:
    def __init__(self, sign: str, index: int, payload: str, second_payload: Optional[str] = None, parsing_needed=False):
        self.sign = sign
        self.index = index
        self.payload = payload
        self.second_payload = second_payload

        if parsing_needed:
            self.payload, self.second_payload = self.parse_payloads()

    @property
    def is_replacement(self):
        return self.sign == REPLACEMENT_MARK

    def __str__(self):
        payload, second_payload = self.fix_payloads()
        if self.is_replacement:
            payload += f"{REPLACEMENT_SPLIT_MARK}{second_payload}"
        return f"{self.sign}{self.index}{INDEX_PAYLOAD_SEPERATOR_MARK}{payload}"

    def __eq__(self, other):
        if (type(
                other) is DeltaElement and other.sign == self.sign and other.index == self.index and other.payload == self.payload and other.second_payload == self.second_payload):
            return True
        return False

    def fix_payloads(self):
        fixed_payload, fixed_second_payload = self.payload, self.second_payload
        for possible_sign in [UNMARK_MARK] + REGULAR_MARKS:
            fixed_payload = replace_signs(fixed_payload, possible_sign, UNMARK_MARK + possible_sign)
            if self.is_replacement:
                fixed_second_payload = fixed_second_payload.replace(possible_sign, UNMARK_MARK + possible_sign)
        return fixed_payload, fixed_second_payload

    def parse_payloads(self):
        if self.sign == REPLACEMENT_MARK:
            payloads = list(split_payload(self.payload))
        else:
            payloads = [self.payload, None]
        for i, payload in enumerate(payloads):
            if not payload:
                continue
            for possible_sign in REGULAR_MARKS:
                payload = payload.replace(UNMARK_MARK + possible_sign, possible_sign)
            payloads[i] = payload.replace(UNMARK_MARK + UNMARK_MARK, UNMARK_MARK)
        return payloads

    def apply_on_data(self, base_data: str, apply_on_reverse=False, offset=0):
        data_with_delta = base_data
        sign = self.sign
        index = self.index
        delta_payload = self.payload

        if apply_on_reverse:
            if sign == DELETION_MARK:
                data_with_delta = (base_data[0: index + offset] + delta_payload + base_data[index + offset:])
                offset += len(delta_payload)
            if sign == INSERTION_MARK:
                data_with_delta = (base_data[0: index + offset] + base_data[index + len(delta_payload) + offset:])
                offset -= len(delta_payload)
            if sign == REPLACEMENT_MARK:
                data_with_delta = (base_data[0: index + offset] + delta_payload + base_data[index + len(
                    self.second_payload) + offset:])
                offset += len(delta_payload) - len(self.second_payload)

        else:
            if sign == DELETION_MARK:
                data_with_delta = (base_data[0:index] + base_data[index + len(delta_payload):])
            if sign == INSERTION_MARK:
                data_with_delta = base_data[0:index] + delta_payload + base_data[index:]
            if sign == REPLACEMENT_MARK:
                data_with_delta = (
                            base_data[0:index] + self.second_payload + base_data[index + len(delta_payload):])

        return data_with_delta, offset


def parse_str_delta_element(str_delta: str) -> DeltaElement:
    sign = str_delta[0]
    index, payload = str_delta[1:].split(INDEX_PAYLOAD_SEPERATOR_MARK, 1)
    index = int(index)

    return DeltaElement(sign=sign, index=index, payload=payload, parsing_needed=True)