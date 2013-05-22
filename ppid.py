# encoding: utf-8
import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="得到程序调用者的PID。在Windows console窗口调用时，相当于获取当前cmd.exe的PID。",
        epilog=EPILOG,
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    print( os.getppid() )

if __name__ == '__main__':
    Main()