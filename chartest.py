import os
import encodings
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Detect string encoding",
        epilog=EPILOG,
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="Target File.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        text = os.sys.stdin.buffer.read(1024*1024)
    else:
        with open(opt.file, "rb") as fileobj:
            text = fileobj.read(1024*1024)
    
    oks = []
    for e in encodings.aliases.aliases.keys():
        try:
            t = text.decode(e)
            oks.append(e)
        except:
            pass
    
    if not oks:
        print("Unknown")
    else:
        for e in oks:
            print(e)

if __name__ == '__main__':
    Main()
