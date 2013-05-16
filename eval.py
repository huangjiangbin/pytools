import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Computer math expression stirng.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "anything",
        metavar="ANY_THING",
        nargs="*",
        help="Math expression stirng.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    line = "".join(opt.anything)
    if not line:
        print("0")
    else:
        print(eval(line))

if __name__ == '__main__':
    Main()
