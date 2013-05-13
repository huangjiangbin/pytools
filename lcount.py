import os
import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Line count",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        help="File encode. Default o ascii"
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="The file. Default to -, means read from stdin.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        lines = os.sys.stdin.readlines()
    else:
        if opt.encoding:
            with open(opt.file, "r", encoding=opt.encoding) as fobj:
                lines = fobj.readlines()
        else:
            try:
                with open(opt.file, "r", encoding="utf-8") as fobj:
                    lines = fobj.readlines()
            except:
                try:
                    with open(opt.file, "r", encoding="gb18030") as fobj:
                        lines = fobj.readlines()
                except:
                    try:
                        with open(opt.file, "r", encoding="iso-8859-1") as fobj:
                            lines = fobj.readlines()
                    except:
                        raise
    
    print(len(lines))
    
if __name__ == '__main__':
    Main()

