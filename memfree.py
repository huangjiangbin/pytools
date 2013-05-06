import ctypes
from ctypes.wintypes import *
import argparse
from inc import EPILOG

DWORDLONG = ctypes.c_uint64

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
            ("dwLength", DWORD ),
            ("dwMemoryLoad", DWORD ),
            ("ullTotalPhys", DWORDLONG ),
            ("ullAvailPhys", DWORDLONG ),
            ("ullTotalPageFile", DWORDLONG ),
            ("ullAvailPageFile", DWORDLONG ),
            ("ullTotalVirtual", DWORDLONG ),
            ("ullAvailVirtual", DWORDLONG ),
            ("ullAvailExtendedVirtual", DWORDLONG ),
         
        ]

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="get global memory status",
        epilog=EPILOG,
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    info = MEMORYSTATUSEX()
    info.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx( ctypes.byref(info) )
    
    G = 1024*1024*1024
    print("          MemoryLoad: %.2f %%"%(info.dwMemoryLoad))
    print("           TotalPhys: %.3f G"%(info.ullTotalPhys/G))
    print("           AvailPhys: %.3f G"%(info.ullAvailPhys/G))
    print("       TotalPageFile: %.3f G"%(info.ullTotalPageFile/G))
    print("       AvailPageFile: %.3f G"%(info.ullAvailPageFile/G))
    print("        TotalVirtual: %.3f G"%(info.ullTotalVirtual/G))
    print("        AvailVirtual: %.3f G"%(info.ullAvailVirtual/G))
    print("AvailExtendedVirtual: %.3f G"%(info.ullAvailExtendedVirtual/G))

if __name__ == '__main__':
    Main()










