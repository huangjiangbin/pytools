import os
import heapq
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Sort file lines.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-n", "--numberic",
        dest="numberic",
        action="store_true",
        help="Sort lines by first column in numberic order",
        )
    parser.add_argument(
        "-r", "--reverse",
        dest="reverse",
        action="store_true",
        help="Sort in desc.",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="Target file. Default to - means read from stdin.",
        )
    return parser, parser.parse_args()

def GetLineNumber(line, flag):
    if flag:
        flag = -1
    else:
        flag = 1
        
    ns = b""
    for c in line:
        c = chr(c).encode("ascii")
        if c in b"0123456789 ":
            ns += c
        else:
            break
        
    return int(ns) * flag

def Main():
    parser, opt = ParseCommandLine()    
    lines = []
    if opt.file == "-":
        lines = os.sys.stdin.buffer.readlines()
    else:
        with open(opt.file, "rb") as fileobj:
            lines = fileobj.readlines()
    
    if not lines:
        return
    
    if opt.numberic:
 
        lines2 = []
        for line in lines:
            heapq.heappush( lines2, (GetLineNumber(line, opt.reverse), line) )
            
        while lines2:
            row = heapq.heappop(lines2)
            line = row[1]
            if not line.endswith(b"\n") and not line.endswith(b"\r"):
                line += b"\r\n"
            os.sys.stdout.buffer.write(line)
    else:
        lines.sort()
        if opt.reverse:
            lines.reverse()
        for line in lines:
            if not line.endswith(b"\n") and not line.endswith(b"\r"):
                line += b"\r\n"
            os.sys.stdout.buffer.write(line)
        
if __name__ == '__main__':
    Main()
