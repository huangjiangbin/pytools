# encoding: utf-8
import time
import datetime
import argparse

from dateutil.parser import parse as strtimeparse

from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="timestamp和时间格式互换工具。如果不使用-r选项，后面应该跟时间字符串，表示将时间字符串转化成timestamp数值。而使用-r选项，则应该跟timestamp数值，表示将timestamp转成时间字符串。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-r", "--reverse",
        dest="reverse",
        action="store_true",
        help="将timestamp格式转化成时间格式。不指定该选项，则表示将时间格式转化成timestamp格式。",
        )
    parser.add_argument(
        "time",
        metavar="TIME/TIMESTAMP",
        nargs="?",
        default="0",
        help="时间值。可以是timestamp类型，也可以是时间字符串。如果不指定，则使用当然时间值。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.reverse:
        if opt.time == "0":
            opt.time = time.time()        
        t = datetime.datetime.fromtimestamp(int(opt.time))
        print(t)
    else:
        if opt.time == "0":
            print(int(time.time()))
        else:
            t = strtimeparse(opt.time)
            print(int(time.mktime(t.timetuple())))


if __name__ == '__main__':
    Main()
