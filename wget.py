import os
from urllib.request import urlopen
import argparse
from inc import EPILOG

def _smart_unicode(s):
    try:
        return s.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return s.decode("gb18030")
        except UnicodeDecodeError:
            try:
                return s.decode("ISO-8859-1")
            except UnicodeDecodeError:
                return ""

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Simple url download tool.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        action="store",
        default="-",
        help="Save the url content to the file. Default to -, means print out to stdout.",
        )
    parser.add_argument(
        "-u", "--unicode",
        dest="unicode",
        action="store_true",
        help="Treat URL content as unicode string. So the print out in Windows Console us readable by human.",
        )
    parser.add_argument(
        "url",
        metavar="URL",
        nargs=1,
        help="URL to get.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    target_url = opt.url[0]
    
    t = urlopen(target_url).read()
    
    if opt.output == "-":
        if opt.unicode:
            t = _smart_unicode(t)
            print(t)
        else:
            os.sys.stdout.buffer.write(t)
            os.sys.stdout.flush()
    else:
        with open(opt.output, "wb") as fileobj:
            fileobj.write(t)

if __name__ == '__main__':
    Main()
