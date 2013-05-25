# encoding: utf-8
import os
import time
import datetime
import subprocess
import argparse
from inc import EPILOG
from func import StdinSize

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="统计程序执行时间",
        epilog=EPILOG,
        )
    parser.add_argument(
        "args",
        metavar="ARG",
        nargs="*",
        help="程序及参数。",
        )
    return parser, parser.parse_args()


def Main():
    stime = time.time()
    parser, opt = ParseCommandLine()
    
    cmd = " ".join(opt.args)
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
    bufsize = StdinSize()
    if bufsize > 0:
        proc.communicate( os.sys.stdin.buffer.read() )
    proc.wait()
    
    etime = time.time()
    dtime = etime-stime
    
    print("")
    print("-"*70)
    print("   Command: %s"%(cmd))
    print("Begin Time: %s %.2f"%(str(datetime.datetime.fromtimestamp(stime)), stime))
    print("  End Time: %s %.2f"%(str(datetime.datetime.fromtimestamp(etime)), etime))
    print(" Used Time: %.2f"%(dtime))
    
if __name__ == '__main__':
    Main()
