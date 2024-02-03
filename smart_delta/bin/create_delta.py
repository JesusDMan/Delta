from smart_delta.src import delta_utils, generate_delta, apply_delta


def main():
    data_1 = (
        "Hello! My name is John Cena. %, + and - are signs used for parsing the delta. "
        "In addition, there's | and $. \\ is used to mark usage of safe signs in the text."
    )
    data_2 = (
        "Hello! My name is Jeff Bazos. There are signs used for parsing the delta, such as +, % and -. "
        "There's also $ and |. To mark usage of safe signs in the text, we use \\."
    )

    delta_utils.print_data(data_1)
    print()
    delta_utils.print_data(data_2)
    print()
    delta_list = generate_delta.create_delta_steps_list(data_1, data_2)
    delta = generate_delta.create_delta_string(delta_list)
    print(delta_list)
    print(repr(delta))

    print(generate_delta.parse_delta_steps(delta))
    print(apply_delta.apply_string_delta(data_1, delta))
    print(data_2)
    print("-" * 99)
    print(apply_delta.apply_string_delta(data_2, delta, reverse_delta=True))
    print(data_1)


if __name__ == "__main__":
    main()
