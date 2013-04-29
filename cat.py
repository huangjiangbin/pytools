# encoding: utf-8
import os
import argparse
from inc import EPILOG

def ArgParse():
    parser = argparse.ArgumentParser(
        description="Concatenate FILE(s), or standard input, to standard output.",
        epilog=EPILOG
        )
    parser.add_argument(
        "-n", "--number-lines",
        dest="number_lines",
        action="store_true",
        help="number output lines",
        )    
    parser.add_argument(
        "-s", "--squeeze-blank",
        dest="squeeze_blank",
        action="store_true",
        help="suppress repeated empty output lines",
        )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        default=["-"],
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ArgParse()
    
    for f in opt.files:
        if f == "-":
            fileobj = os.sys.stdin.buffer
        else:
            fileobj = open(f, "rb")
        
        n = 0
        lastlinebreak = False
        while 1:
            n += 1
            
            line = fileobj.readline()
            if not line:
                break
            
            if opt.squeeze_blank and ( not line.strip() ):
                if line.endswith(b"\r\n"):
                    line = b"\r\n"
                elif line.endswith(b"\r"):
                    line = b"\r"
                else:
                    line = b"\n"
            
            if opt.number_lines:
                line = ("%5d "%(n)).encode("ascii") + line
            os.sys.stdout.buffer.write(line)
            
            if line.endswith(b"\n") or line.endswith(b"\r"):
                lastlinebreak = True
            else:
                lastlinebreak = False
                
        if f != "-":
            fileobj.close()
        
        if not lastlinebreak:
            print()

if __name__ == '__main__':
    Main()