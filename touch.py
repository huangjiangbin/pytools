import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Create a file if the file not exists.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs=1,
        help="Target file.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    thefile = opt.file[0]
    if not os.path.isfile(thefile):
        with open(thefile, "wb") as f:
            pass
    else:
        os.utime(thefile)

if __name__ == '__main__':
    Main()
