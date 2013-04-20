import time
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "sleep some times",
        epilog = EPILOG,
        )
    parser.add_argument(
        "-m", "--millisecond",
        dest="millisecond",
        action="store_true",
        help="treat N as millisecond"
        )
    parser.add_argument(
        "n",
        nargs=1,
        type=int,
        help="how many second or millisecond gets to sleep",
        )
    parser.add_argument(
        "-i", "--information",
        dest="information",
        action="store",
        help="output the information before sleep",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    sleeptime = opt.n[0]
    if opt.millisecond:
        sleeptime /= 1000.0
    
    if opt.information:
        print(opt.information)
    
    time.sleep(sleeptime)
    
if __name__ == '__main__':
    Main()