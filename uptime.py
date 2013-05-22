# encoding: utf-8
import os
import ctypes
import datetime
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="显示系统开机时间或从开机到现在经过的秒数。默认是显示开机时间。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-c", "--tickcount",
        dest="tickcount",
        action="store_true",
        help="显示从开机到现在经过的秒数。"
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    now = datetime.datetime.now()
    try:
        tickcount = ctypes.windll.kernel32.GetTickCount64()
    except:
        tickcount = ctypes.windll.kernel32.GetTickCount()
    
    if opt.tickcount:
        print(tickcount)
    else:
        d = datetime.timedelta(0, tickcount/1000, tickcount%1000)
        btime = now - d
        print(btime.strftime("%Y-%m-%d %H:%M:%S"))
        
if __name__ == '__main__':
    Main()
    