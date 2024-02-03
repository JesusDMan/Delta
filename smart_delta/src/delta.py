from typing import Optional

from smart_delta.src import (
    REPLACEMENT_MARK,
    REPLACEMENT_SPLIT_MARK,
    INDEX_PAYLOAD_SEPERATOR_MARK,
)


class Delta:
    def __init__(
        self, sign: str, index: int, payload: str, second_payload: Optional[str] = None
    ):
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
        if (
            type(other) is Delta
            and other.sign == self.sign
            and other.index == self.index
            and other.payload == self.payload
            and other.second_payload == self.second_payload
        ):
            return True
        return False
