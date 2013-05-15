import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Reduce same lines.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="Target file. Default to - means read from stdin.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = open(opt.file, "rb")
    
    lastline = None
    while True:
        line = fileobj.readline()
        if not line:
            break
        if line != lastline:
            os.sys.stdout.buffer.write(line)
            lastline = line
    
    if not opt.file == "-":
        fileobj.close()
    
if __name__ == '__main__':
    Main()
