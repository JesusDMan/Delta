from smart_delta.src import UNMARK_MARK


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
