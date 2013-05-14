import os
import datetime
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Get file stat info.",
        epilog=EPILOG,
        conflict_handler="resolve"
        )
    parser.add_argument(
        "-h", "--human-readable",
        dest="human",
        action="store_true",
        help="Show file size in human-readable format."
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs=1,
        help="Target file.",
        )
    return parser, parser.parse_args()

def SFormat(v, flag):
    if not flag:
        return v
    G = 1024*1024*1024
    M = 1024*1024
    K = 1024
    if v > G:
        return "%.2f G"%(v/G)
    if v > M:
        return "%.2f M"%(v/M)
    if v > K:
        return "%.2f K"%(v/K)
    return "%d B"%(v)

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file[0] == "-":
        filepath = os.sys.stdin.read().strip()
    else:
        filepath = opt.file[0]
    abspath = os.path.realpath(filepath)
    
    if (not filepath) or (not os.path.exists(abspath)):
        print("Can't find the file %s"%(filepath))
        os.sys.exit(1)
        
    info = os.stat(abspath)
    ext = os.path.splitext(abspath)[1]
    filename = os.path.split(abspath)[1]
    
    print("  Absolute Path: %s"%(abspath))
    print("   Is Directory: %s"%(os.path.isdir(abspath)))
    if os.path.isfile(abspath):
        print("      File Name: %s"%(filename))
        print("      Extention: %s"%(ext))
        print("           Size: %s"%(SFormat(info.st_size, opt.human)))
    print("    Create Time: %s"%(datetime.datetime.fromtimestamp(info.st_ctime)))
    print("    Modify Time: %s"%(datetime.datetime.fromtimestamp(info.st_mtime)))
if __name__ == '__main__':
    Main()
