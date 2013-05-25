# encoding: utf-8
import os
import argparse
from inc import EPILOG
from func import StdoutWrite, StripCRLF

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="将文件中的所有行连接成一行。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        default="utf-8",
        help="连接符的编码。",
        )
    parser.add_argument(
        "-s", "--separator",
        dest="separator",
        action="store",
        default="",
        help="连接符。默认为空字符串。如果使用的是多字节字符，则需要指定编码。",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="目标文件。默认为“-”，表示从标准输入中读取文件内容。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        lines = os.sys.stdin.buffer.readlines()
    else:
        with open(opt.file, "rb") as fileobj:
            lines = fileobj.readlines()
    
    sep = opt.separator.encode( opt.encoding )
    lines = [StripCRLF(line) for line in lines]
    StdoutWrite(sep.join(lines))

if __name__ == '__main__':
    Main()
