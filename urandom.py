import os
import argparse
from inc import epilog

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="generate random bytes",
        epilog=epilog,
        )
    parser.add_argument(
        "-l", "--length",
        dest="length",
        action="store",
        type=int,
        help="byte length",
        required=True,
        )
    args = parser.parse_args()
    return parser, args

def Main():
    parser, opt = ParseCommandLine()
    if opt.length < 1:
        print("byte length must be larger than 0")
        os.sys.exit(1)
        
    os.sys.stdout.buffer.write(os.urandom(opt.length))
    
if __name__ == '__main__':
    Main()