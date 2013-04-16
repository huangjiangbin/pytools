import datetime
import locale
import argparse
from inc import epilog


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "Show current sytem time",
        epilog = epilog,
        )
    parser.add_argument(
        "-u", "--utc", "--universal",
        dest="utc",
        action="store_true",
        help="print or set Coordinated Universal Time",
        )
    parser.add_argument(
        "-f", "--format",
        dest="format",
        action="store",
        default="%Y-%m-%d %H:%M:%S",
        help="format the output",
        )
    return parser, parser.parse_args()

def Main():
    parse, opt = ParseCommandLine()
    print( opt.format )
    
    if opt.utc:
        now = datetime.datetime.utcnow()
    else:
        now = datetime.datetime.now()
    
    result = now.strftime(opt.format)
    print(type(result))

if __name__ == '__main__':
    Main()