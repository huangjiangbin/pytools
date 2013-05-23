# encoding: utf-8
import os
import argparse

import chardet

from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="测试文件编码。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="目标文件。默认为“-”表示从标准输入中读取。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        content = os.sys.stdin.buffer.raw.read()
    else:
        with open(opt.file, "rb") as fileobj:
            content = fileobj.read()
    
    info = chardet.detect(content)
    print("  encoding: %s"%(info["encoding"]))
    print("confidence: %.2f"%(info["confidence"]))

if __name__ == '__main__':
    Main()
