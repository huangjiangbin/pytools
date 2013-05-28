# encoding: utf-8
import os
import argparse
from inc import EPILOG
from func import StdoutWrite


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="删除或合并空白行。",
        )
    parser.add_argument(
        "-r", "--reduce",
        dest="reduce",
        action="store_true",
        help="合并空白行，连续多个空白行将被合并成一个空白行。否则删除所有空白行。",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="目标文件。默认为“-”，表示从标准输入中读取内容。",
        )
    return parser, parser.parse_args()


def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        lines = os.sys.stdin.buffer.readlines()
    else:
        with open(opt.file, "rb") as fileobj:
            lines = fileobj.readlines()
    
    if opt.reduce:
        lines2 = []
        blanklineflag = False
        for line in lines:
            if line.strip():
                blanklineflag = False
                lines2.append( line )
            else:
                if not blanklineflag:
                    blanklineflag = True
                    lines2.append( line )
        StdoutWrite(b"".join(lines2))
    else:
        lines2 = []
        for line in lines:
            if line.strip():
                lines2.append(line)
        StdoutWrite(b"".join(lines2))
        
if __name__ == '__main__':
    Main()



