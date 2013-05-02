import os
import re
import datetime
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="show the day's iso week number",
        epilog=EPILOG,
        )
    parser.add_argument(
        "day",
        metavar="DAY",
        nargs="?",
        default="0",
        help="day. e.g. 2013-05-02 or 2013-5-2 or 20130502",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.day == "0":
        theday = datetime.datetime.now()
    else:
        info = re.match("(\d{4})-?(\d{1,2})-?(\d{1,2})", opt.day).groups()
        theday = datetime.datetime(int(info[0]), int(info[1]), int(info[2]), 10, 10, 10)
    print(theday.isocalendar()[1])

if __name__ == '__main__':
    Main()
    