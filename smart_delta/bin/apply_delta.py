import argparse
import os
from typing import Optional

from smart_delta.src import delta_applier


def apply_delta_on_file(base_filepath: str, delta_filepath: str, new_filepath: str, reversed: bool = False,
                        base_dir: Optional[str] = None):
    if base_dir:
        os.chdir(base_dir)

    with open(base_filepath, "rb") as f:
        data_1 = f.read()
    with open(delta_filepath, "rb") as f:
        delta = f.read()

    with open(new_filepath, "wb") as f:
        delta = delta_applier.DeltaApplier(delta)
        f.write(delta.apply_on_data(data_1, reverse_delta=reversed))


def main():
    parser = argparse.ArgumentParser(prog="DeltaApplier")
    parser.add_argument("-b", "--base_file", type=str, required=True)
    parser.add_argument("-d", "--delta_file", type=str, required=True)
    parser.add_argument("-f", "--new_file", type=str, required=True)
    parser.add_argument("-o", "--base_dir", "--dir", type=str)
    parser.add_argument("-r", "--reversed", action="store_true")
    args = parser.parse_args()
    apply_delta_on_file(base_filepath=args.base_file, delta_filepath=args.delta_file, new_filepath=args.new_file,
                        reversed=args.reversed, base_dir=args.base_dir)


if __name__ == "__main__":
    main()
