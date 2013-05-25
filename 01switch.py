# encoding: utf-8
import os
import random
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="0/1控制器。程序运行后随机地以0或1退出。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-p", "--percent",
        dest="percent",
        action="store",
        type=float,
        default=50.0,
        help="0值退出的百分比概率。如30表示，程序生成0值的概率是30%。默认概率是50%。"
        )
    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="打印退出值。"
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    p = int(opt.percent * 1000)
    d = random.randint(0, 100*1000)
    if d <= p:
        r = 0
    else:
        r = 1
    
    if opt.verbose:
        print(r)
    os.sys.exit(r)

if __name__ == '__main__':
    Main()
