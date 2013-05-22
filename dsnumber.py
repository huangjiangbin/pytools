# encoding: utf-8
import os
import wmi
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="获取磁盘序列号工具。",
        epilog=EPILOG,
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    c = wmi.WMI()
    for disk in c.Win32_DiskDrive():
        id = disk.DeviceID
        try:
            sn = disk.SerialNumber
        except:
            sn = "0"*40
        print("%s => %s"%(id, sn))

if __name__ == '__main__':
    Main()
