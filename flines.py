# encoding: utf-8
import os
import argparse
from inc import EPILOG
from func import StdoutWrite

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="显示文件中指定行的内容。允许定义起始行号和终止行号。文件的行编号从1开始；0为无效行号；起始行号为0时，表示最开始行，即为1。终止行号为0时，表示最后一行，相当于-1。起始行号和终止行号所对应的行内容包含在将被显示内容中。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-b", "--begin",
        dest="begin",
        action="store",
        type=int,
        default=0,
        help="起始行号。1表第1行，2表示第2行；-1表示最后第1行；-2表示最后第2行。以此类推。。",
        )
    parser.add_argument(
        "-e", "--end",
        dest="end",
        action="store",
        type=int,
        default=0,
        help="终止行号。",
        )
    parser.add_argument(
        "-n", "--number",
        dest="number",
        action="store_true",
        help="显示原始行号。",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="目标文件。默认为“-”，表示从标准输入读取内容。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        lines = os.sys.stdin.buffer.readlines()
    else:
        with open(opt.file, "rb") as fileobj:
            lines = fileobj.readlines()
        
    lastline = lines[-1]
    if not ( lastline.endswith(b"\r") or lastline.endswith(b"\n") ):
        lastline += os.linesep.encode("ascii")
    lines[-1] = lastline
        
    begin = opt.begin
    if begin == 0:
        begin = None
    elif begin > 0:
        begin -= 1
    else:
        begin += 1
    if begin == 0:
        begin = None
    
    end = opt.end
    if end == 0:
        end = None
    elif end < 0:
        end += 1
    if end == 0:
        end = None
    
    if not opt.number:
        StdoutWrite(b"".join(lines[begin:end]))
    else:
        lines2 = []
        if begin is None:
            lineno = 1
        else:
            lineno = begin + 1
        for line in lines[begin:end]:
            line = ( "%4d "%(lineno) ).encode("ascii") + line
            lines2.append( line )
            lineno += 1
        StdoutWrite(b"".join(lines2))
    
if __name__ == '__main__':
    Main()
