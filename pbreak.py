# encoding: utf-8
import os
import argparse
from inc import EPILOG
from cmdsize import GetConsoleScreenSize
from getchar import GetChar
from func import StdoutWrite

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Look a file page by page.",
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
    
    cmdsize = GetConsoleScreenSize()
    height = cmdsize[1]
    
    if opt.file == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = open(opt.file, "rb")
    
    n = 0
    while True:
        line = fileobj.readline()
        if not line:
            break
        
        StdoutWrite(line)
        
        n += 1
        if n%(height-1) == 0:
            msg = GetChar("-- MORE -- ")
            print("")
            
            if msg in [b"\x1b", b"\x03", b"q", b"Q"]: # press ESC, Ctrl+C, q, Q to exit
                break
            
    if opt.file != "-":
        fileobj.close()

if __name__ == '__main__':
    Main()
