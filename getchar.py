# encoding: utf-8
import os
import io
import argparse
from inc import EPILOG
import msvcrt

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "测试按键值。普通键获得1个字节内容；部分功能键获得2个字节内容。",
        epilog = EPILOG,
        )
    parser.add_argument(
        "-i", "--information",
        dest="information",
        action="store",
        help="进入按键测试前显示的内容。",
        )
    parser.add_argument(
        "-e", "--echo",
        dest="echo",
        action="store_true",
        help="将按键内容打印到标准输出中。",
        )
    return parser, parser.parse_args()

def GetChar(prompt):
    if prompt:
        print(prompt, end="", flush=True)
        
    msg = msvcrt.getch()
    while msvcrt.kbhit():
        msg += msvcrt.getch()
    
    return msg

def Main():
    parser, opt = ParseCommandLine()
    
    msg = GetChar(opt.information)
    
    if opt.echo:
        print(opt.information, end="", flush=True)
    
if __name__ == '__main__':
    Main()
