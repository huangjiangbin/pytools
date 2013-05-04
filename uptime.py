import os
import ctypes
import datetime
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Show system boot time or milliseconds elapsed since the system boot.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-c", "--tickcount",
        dest="tickcount",
        action="store_true",
        help="Show the number of milliseconds that have elapsed since the system was started. Otherwise show boot time in format like \"2013-05-04 03:32:03\"."
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
    