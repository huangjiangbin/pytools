import os
import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="list files under given folder.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-r", "--recursive",
        dest="recursive",
        action="store_true",
        help="list subdirectories recursively",
        )
    parser.add_argument(
        "-d", "--show-directories",
        dest="showdirectories",
        action="store_true",
        help="show directories",
        )
    parser.add_argument(
        "folder",
        metavar="FOLDER",
        nargs="?",
        default=".",
        help="target folder. default to current folder.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    folder = os.path.realpath(opt.folder)
    if not opt.recursive:
        fs = os.listdir(folder)
        for f in fs:
            ff = os.path.realpath( os.path.join(folder, f) )
            if (not opt.showdirectories) and os.path.isdir(ff):
                continue
            print(ff)
    else:
        for root, dirs, files in os.walk(folder):
            if opt.showdirectories:
                print(root)
            for f in files:
                ff = os.path.join(root, f)
                print(ff)
    

if __name__ == '__main__':
    Main()




