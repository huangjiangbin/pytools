import re
import datetime
import locale
import argparse
from inc import epilog

def strftime(datetimeobject, formatstring):
    formatstring = formatstring.replace("%%", "guest_u_never_use_20130416")
    ps = list(set(re.findall("(%.)", formatstring)))
    format2 = "|".join(ps)
    vs = datetimeobject.strftime(format2).split("|")
    for p, v in zip(ps, vs):
        formatstring = formatstring.replace(p, v)
    return formatstring.replace("guest_u_never_use_20130416", "%")

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
    
    if opt.utc:
        now = datetime.datetime.utcnow()
    else:
        now = datetime.datetime.now()
    
    result = strftime(now, opt.format)
    print(result)

if __name__ == '__main__':
    Main()