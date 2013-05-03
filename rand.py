import random
import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="random number generator",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-s", "--start",
        dest="start",
        action="store",
        type=int,
        default=0,
        help="rand int area start",
        )
    parser.add_argument(
        "-e", "--end",
        dest="end",
        action="store",
        type=int,
        default=100,
        help="rand int area end",
        )
    parser.add_argument(
        "-f", "--float",
        dest="float",
        action="store_true",
        help="generate float number in [0.0, 1.0)",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.float:
        print( random.random() )
    else:
        print( random.randint(opt.start, opt.end) )

if __name__ == '__main__':
    Main()