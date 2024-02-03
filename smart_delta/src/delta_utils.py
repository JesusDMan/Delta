from smart_delta.src import (UNMARK_MARK, REPLACEMENT_SPLIT_MARK, )


def print_data(data):
    print(" ".join([str(i) for i in range(len(data))]))
    print("".join([data[i] + " " * len(str(i)) for i in range(len(data))]))


def find_system_marks(string, marks):
    indices = []
    is_after_mark = False

    for i, char in enumerate(string):
        if char == UNMARK_MARK:
            if is_after_mark:
                is_after_mark = False
            else:
                is_after_mark = True

        if char != UNMARK_MARK and is_after_mark:
            is_after_mark = False

        elif char in marks and not is_after_mark:
            indices.append(i)
    return indices


def split_payload(payload: str):
    split_index = find_system_marks(payload, (REPLACEMENT_SPLIT_MARK,))[0]
    return payload[:split_index], payload[split_index + 1:]


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
