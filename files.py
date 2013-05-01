import os
import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="list files under given folder.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-r", "--recurrent",
        dest="recurrent",
        action="store_true",
        help="show files under sub-folders.",
        )
    parser.add_argument(
        "-a", "--absolute",
        dest="absolute",
        action="store_true",
        help="show absolute path of the files.",
        )
    parser.add_argument(
        "-o", "--only-files",
        dest="onlyfiles",
        action="store_true",
        help="show only files",
        )
    parser.add_argument(
        "folder",
        metavar="FOLDER",
        nargs="?",
        default=".",
        help="target folder. default to current folder.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    print(opt)

if __name__ == '__main__':
    Main()