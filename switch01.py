import os
import random
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="exit with code 0 or 1 randomly.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-p", "--percent",
        dest="percent",
        action="store",
        type=float,
        default=50.0,
        help="30 means exit code will be 0 by 30%% possibility"
        )
    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="display the result."
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    p = int(opt.percent * 1000)
    d = random.randint(0, 100*1000)
    if d <= p:
        r = 0
    else:
        r = 1
    
    if opt.verbose:
        print(r)
    os.sys.exit(r)

if __name__ == '__main__':
    Main()
