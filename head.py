import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Show head lines of a file.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-f", "--file",
        dest="file",
        action="store",
        default="-",
        help="Target file.",
        )
    parser.add_argument(
        "-n", "--number",
        dest="number",
        action="store",
        type=int,
        default=0,
        help="Show top N lines",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    print(opt)
    
if __name__ == '__main__':
    Main()
