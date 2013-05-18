# encoding: utf-8
import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="如果文件不存在，则创建；如果文件存在，则更新文件的最后修改时间。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs=1,
        help="目标文件。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    thefile = opt.file[0]
    if not os.path.isfile(thefile):
        with open(thefile, "wb") as f:
            pass
    else:
        os.utime(thefile)

if __name__ == '__main__':
    Main()
