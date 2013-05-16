import os
import argparse
from inc import EPILOG
from func import StripCRLF

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Show head lines of a file.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        default="utf-8",
        help="File encoding. Default to UTF-8."
        )
    parser.add_argument(
        "-l", "--line-number",
        dest="number",
        action="store_true",
        help="Show line number.",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
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
    
    if opt.file == "-":
        fileobj = os.sys.stdin
    else:
        fileobj = open(opt.file, "r", encoding=opt.encoding)
    
    num = 0
    for x in range(0, opt.number):
        num += 1
        
        line = fileobj.readline()
        if not line:
            break
        
        line = StripCRLF(line)
        
        if opt.number:
            print("%5d %s"%(num, line))
        else:
            print(line)
    
    if opt.file != "-":
        fileobj.close()
    
if __name__ == '__main__':
    Main()
