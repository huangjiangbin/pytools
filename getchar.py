import os
import io
import argparse
from inc import EPILOG
import msvcrt

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "Gets a single character from standard input. Does not echo to the screen.",
        epilog = EPILOG,
        )
    parser.add_argument(
        "-i", "--information",
        dest="information",
        action="store",
        help="output the information before wait for input",
        )
    parser.add_argument(
        "-e", "--echo",
        dest="echo",
        action="store_true",
        help="echo the input character",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.information:
        print(opt.information)
    
    msg = msvcrt.getch()
    while msvcrt.kbhit():
        msg += msvcrt.getch()
    
    if opt.echo:
        os.sys.stdout.buffer.write(msg)
        os.sys.stdout.buffer.flush()
    
if __name__ == '__main__':
    Main()