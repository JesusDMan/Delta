from smart_delta.src import delta_utils, delta_generator, apply_delta, delta_applier


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
    delta_ = delta.DeltaApplier(data_1, data_2, generate_delta.generate_delta)
    print(delta_.delta_elements)
    delta_ = str(delta_)
    print(repr(delta_))

    print(apply_delta.apply_on_data(data_1, delta_))
    print(data_2)
    print("-" * 99)
    print(apply_delta.apply_on_data(data_2, delta_, reverse_delta=True))
    print(data_1)


if __name__ == "__main__":
    main()
