# encoding: utf-8
import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="文件或字节流大小统计工具。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="目标文件或字节流。默认为“-”，表示从标准输入中读取的字节流。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        try:
            size = len( os.sys.stdin.buffer.raw.read() )
        except:
            size = 0
    else:
        size = os.stat(opt.file).st_size
    
    print(size)

if __name__ == '__main__':
    Main()
