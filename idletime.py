import ctypes
from ctypes.wintypes import *
import argparse
from inc import EPILOG

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("dwTime", DWORD),
    ]

def GetLastInputInfo():
    info = LASTINPUTINFO()
    info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    r = ctypes.windll.user32.GetLastInputInfo( ctypes.byref(info) )
    return info.dwTime

def GetTickCount():
    return ctypes.windll.kernel32.GetTickCount()

def GetIdleCount():
    return GetTickCount() - GetLastInputInfo()

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Get keyboard/mouse idle time. By default show the idle time in seconds.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-m", "--milliseconds ",
        dest="milliseconds",
        action="store_true",
        help="Show idle time in million seconds.",
        )
    parser.add_argument(
        "-M", "--minutes",
        dest="minutes",
        action="store_true",
        help="Show idle time in minutes."
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    idletime = GetIdleCount()
    if opt.milliseconds:
        print(idletime)
    elif opt.minutes:
        print( int( idletime / (60*1000) ) )
    else:
        print( int( idletime / 1000 ) )

if __name__ == '__main__':
    Main()
