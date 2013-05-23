# encoding: utf-8
import os
import argparse
import wmi
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="获取CPU信息。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="显示为详情模式。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    dc = wmi.WMI()
    cpus = dc.Win32_Processor()
    
    if opt.verbose:
        for info in cpus:
            print(info)
    else:
        print("-"*40)
        for info in cpus:
            print("%s: %s"%("         DeviceID", info.DeviceID))
            print("%s: %s"%("             Name", info.Name))
            print("%s: %s"%("      Description", info.Description))
            print("%s: %s"%("    NumberOfCores", info.NumberOfCores))
            print("%s: %s MHz"%("CurrentClockSpeed", info.CurrentClockSpeed))
            
            print("-"*40)
        
if __name__ == '__main__':
    Main()
