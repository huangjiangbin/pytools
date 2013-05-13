import os
import argparse
from inc import EPILOG

import win32com.client
import pythoncom

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Get files/folders size",
        epilog=EPILOG,
        conflict_handler="resolve"
        )
    parser.add_argument(
        "-h", "--human-readable",
        dest="human",
        action="store_true",
        help="Show file size in human readable format",
        )
    parser.add_argument(
        "-s", "--single",
        dest="single",
        action="store_true",
        help="Show single file size",
        )
    parser.add_argument(
        "folder",
        metavar="FOLDER",
        nargs="?",
        default=".",
        help="Target folder",
        )
    return parser, parser.parse_args()

def GetFileSize(f):
    info = os.stat(f)
    return info.st_size

def GetFolderSizeQuick(target_folder):
    fso = win32com.client.Dispatch("Scripting.FileSystemObject")
    fobj = fso.GetFolder(target_folder)
    return fobj.size

def GetFolderSize(target_folder):
    fsize = 0
    for root, folder, files in os.walk(target_folder):
        for f in files:
            fsize += os.path.getsize(os.path.join(root, f))
    return fsize

def SizeFormat(fsize, flag):
    if not flag:
        return "%16d"%(fsize)
    
    G = 1024*1024*1024
    M = 1024*1024
    K = 1024
    
    if fsize >= G:
        return "%14.2f G"%(fsize/G)
    if fsize >= M:
        return "%14.2f M"%(fsize/M)
    if fsize >= K:
        return "%14.2f K"%(fsize/K)
    return "%11d.00 B"%(fsize)
    
def Main():
    parser, opt = ParseCommandLine()
    
    target_folder = os.path.realpath(opt.folder)
    if opt.single:
        if os.path.isdir(target_folder):
            fsize = GetFolderSize(target_folder)
            flag = "D"
        elif os.path.isfile(target_folder):
            fsize = os.path.getsize(target_folder)
            flag = "F"
        else:
            fsize = 0
            flag = "X"
        print("%s %s %s"%(SizeFormat(fsize, opt.human), flag, target_folder))
    else:
        for root, folders, files in os.walk(target_folder):
            for f in folders:
                f = os.path.join(root, f)
                fsize = GetFolderSize(f)
                flag = "D"
                print("%s %s %s"%(SizeFormat(fsize, opt.human), flag, f))
            for f in files:
                f = os.path.join(root, f)
                fsize = os.path.getsize(f)
                flag = "F"
                print("%s %s %s"%(SizeFormat(fsize, opt.human), flag, f))
            break
if __name__ == '__main__':
    Main()
