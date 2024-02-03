INSERTION_MARK = "+"
DELETION_MARK = "-"
REPLACEMENT_MARK = "%"
REPLACEMENT_SPLIT_MARK = "$"
INDEX_PAYLOAD_SEPERATOR_MARK = "|"
UNMARK_MARK = "\\"
SAFE_MARKS = [
    UNMARK_MARK,  # This has to be the first
    INSERTION_MARK,
    DELETION_MARK,
    REPLACEMENT_MARK,
    REPLACEMENT_SPLIT_MARK,
    INDEX_PAYLOAD_SEPERATOR_MARK,
]

REGULAR_MARKS = [
    INSERTION_MARK,
    DELETION_MARK,
    REPLACEMENT_MARK,
    REPLACEMENT_SPLIT_MARK,
    INDEX_PAYLOAD_SEPERATOR_MARK,
]


def replace_signs(data, to_replace, replace_with):
    is_after_mark = False
    new_data = data
    for index, char in enumerate(data):
        if data[index: index + len(to_replace)] == to_replace and not is_after_mark:
            new_data = (
                    new_data[: index + len(new_data) - len(data)]
                    + replace_with
                    + data[index + len(to_replace):]
            )
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
