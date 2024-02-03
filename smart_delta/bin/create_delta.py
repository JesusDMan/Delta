import argparse
import os
from typing import Optional

from smart_delta.src import delta_generator


def create_delta_file(filepath_1: str, filepath_2: str, delta_filepath: str, base_dir: Optional[str] = None):
    if base_dir:
        os.chdir(base_dir)

    with open(filepath_1, "r") as f:
        data_1 = f.read()
    with open(filepath_2, "r") as f:
        data_2 = f.read()

    delta_ = delta_generator.DeltaGenerator(data_1, data_2)
    delta_ = str(delta_)

    with open(delta_filepath, "w") as f:
        f.write(delta_)


def main():
    parser = argparse.ArgumentParser(prog="DeltaGenerator")
    parser.add_argument("-b", "--base_file", "--file_1", type=str, required=True)
    parser.add_argument("-f", "--other_file", "--file_2", type=str, required=True)
    parser.add_argument("-d", "--delta_file", type=str, required=True)
    parser.add_argument("-o", "--base_dir", "--dir", type=str)
    args = parser.parse_args()

    create_delta_file(filepath_1=args.base_file, filepath_2=args.other_file, delta_filepath=args.delta_file,
                      base_dir=args.base_dir)


if __name__ == "__main__":
    main()
