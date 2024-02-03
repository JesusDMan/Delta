from typing import Optional

from smart_delta.src import REPLACEMENT_MARK, REPLACEMENT_SPLIT_MARK, INDEX_PAYLOAD_SEPERATOR_MARK, UNMARK_MARK, \
    REGULAR_MARKS
from smart_delta.src.delta_utils import *


class Delta:
    def __init__(self, sign: str, index: int, payload: str, second_payload: Optional[str] = None):
        self.sign = sign
        self.index = index
        self.payload = payload
        self.second_payload = second_payload

    @property
    def is_replacement(self):
        return self.sign == REPLACEMENT_MARK

    def __str__(self):
        payload = self.payload
        if self.is_replacement:
            payload += f"{REPLACEMENT_SPLIT_MARK}{self.second_payload}"

        return f"{self.sign}{self.index}{INDEX_PAYLOAD_SEPERATOR_MARK}{payload}"

    def __eq__(self, other):
        if type(other) is Delta and \
                other.sign == self.sign and \
                other.index == self.index and \
                other.payload == self.payload and \
                other.second_payload == self.second_payload:
            return True
        return False


def split_payload(payload: str):
    is_after_mark = False
    split_index = 0
    for i, ch in enumerate(payload):

        if ch == REPLACEMENT_SPLIT_MARK and not is_after_mark:
            split_index = i

        if ch == UNMARK_MARK:
            if is_after_mark:
                is_after_mark = False
            else:
                is_after_mark = True
        if ch != UNMARK_MARK:
            is_after_mark = False
    return payload[:split_index], payload[split_index + 1:]


def parse_str_delta(str_delta: str) -> Delta:
    sign = str_delta[0]
    index, payload = str_delta[1:].split(INDEX_PAYLOAD_SEPERATOR_MARK, 1)
    index = int(index)

    if sign == REPLACEMENT_MARK:
        payloads = list(split_payload(payload))
    else:
        payloads = [payload, None]
    for i, payload in enumerate(payloads):
        if not payload:
            continue
        for possible_sign in REGULAR_MARKS:
            payload = payload.replace(UNMARK_MARK + possible_sign, possible_sign)
        payloads[i] = payload.replace(UNMARK_MARK+UNMARK_MARK, UNMARK_MARK)
    return Delta(sign=sign, index=index, payload=payloads[0], second_payload=payloads[1])
