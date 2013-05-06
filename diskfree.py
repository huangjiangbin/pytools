import ctypes
from ctypes.wintypes import *
import argparse
from inc import EPILOG


ULARGE_INTEGER = ctypes.c_uint64


def GetDisks():
    ds = list( str( bin( ctypes.windll.kernel32.GetLogicalDrives() ) )[2:] )
    ds.reverse()
    disks = []
    didx = ord("A")
    for idx in range(0, len(ds)):
        if ds[idx] == "1":
            disks.append(chr(didx)+":")
        didx += 1
    return disks

def GetDiskFreeSpaceEx(dirname):
    FreeBytesAvailable = ULARGE_INTEGER()
    TotalNumberOfBytes = ULARGE_INTEGER()
    TotalNumberOfFreeBytes = ULARGE_INTEGER()
    
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        dirname,
        ctypes.byref(FreeBytesAvailable),
        ctypes.byref(TotalNumberOfBytes),
        ctypes.byref(TotalNumberOfFreeBytes),
        )
    
    return (
        FreeBytesAvailable.value,
        TotalNumberOfBytes.value,
        TotalNumberOfFreeBytes.value,
    )

def PrintInfo(info, disk, opt):
    G = 1024*1024*1024
    
    if info[0] or info[1] or info[2]:
        if opt.byte:
            print("%s Total: %12d, Free: %12d, Used: %12d"%(
                disk.upper(), info[1], info[2], info[1]-info[2],
                ))
        else:
            print("%s Total: %6.2f G, Free: %6.2f G, Used: %6.2f G"%(
                disk.upper(), info[1]/G, info[2]/G, (info[1]-info[2])/G,
                ))

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="get disk info",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-b", "--byte",
        dest="byte",
        action="store_true",
        help="Show the result in unit of byte.",
    )
    parser.add_argument(
        "disks",
        metavar="DISK",
        nargs="*",
        help="Disk name which it's info will be retrieved. In format c: or c:\\",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if not opt.disks:
        opt.disks = GetDisks()
        
    for disk in opt.disks:
        info = GetDiskFreeSpaceEx(disk)
        PrintInfo(info, disk, opt)
        
if __name__ == '__main__':
    Main()
