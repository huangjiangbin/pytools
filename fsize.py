import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Get file size or stream length.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="Target file. Default to - means read from stdin.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        try:
            size = len( os.sys.stdin.buffer.raw.read() )
        except:
            size = 0
    else:
        size = os.stat(opt.file).st_size
    
    print(size)

if __name__ == '__main__':
    Main()
