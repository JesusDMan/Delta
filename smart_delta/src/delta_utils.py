from smart_delta.src import UNMARK_MARK, REPLACEMENT_SPLIT_MARK, INDEX_PAYLOAD_SEPERATOR_MARK, REPLACEMENT_MARK, \
    REGULAR_MARKS
from smart_delta.src.delta import Delta


def replace_signs(data, to_replace, replace_with):
    is_after_mark = False
    new_data = data
    for index, char in enumerate(data):
        if data[index: index + len(to_replace)] == to_replace and not is_after_mark:
            new_data = (new_data[: index + len(new_data) - len(data)] + replace_with + data[index + len(to_replace):])
        elif char == UNMARK_MARK:
            if is_after_mark:
                is_after_mark = False
            else:
                is_after_mark = True
        elif is_after_mark:
            is_after_mark = False
    return new_data


def print_data(data):
    print(" ".join([str(i) for i in range(len(data))]))
    print("".join([data[i] + " " * len(str(i)) for i in range(len(data))]))


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
        payloads[i] = payload.replace(UNMARK_MARK + UNMARK_MARK, UNMARK_MARK)
    return Delta(sign=sign, index=index, payload=payloads[0], second_payload=payloads[1])
