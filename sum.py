import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Sum lines.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-f", "--float",
        dest="float",
        action="store_true",
        help="Tread lines as float number.",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="Target file.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = open(opt.file, "rb")
    
    number = 0
    while 1:
        line = fileobj.readline()
        if not line:
            break
        
        try:
            if opt.float:
                n = float( line.strip() )
            else:
                n = int( line.strip() )
        except:
            n = 0
        
        number += n
    
    if opt.file != "-":
        fileobj.close()
        
    print(number)

if __name__ == '__main__':
    Main()
