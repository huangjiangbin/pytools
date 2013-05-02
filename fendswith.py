import os
import re
import argparse
from inc import EPILOG
from fstartswith import unescape

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="find files endswith given string",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        default="utf-8",
        help="file encoding.",
        )
    parser.add_argument(
        "-s", "--search",
        dest="search",
        action="store",
        required=True,
        help="the given string.",
        )
    parser.add_argument(
        "-p", "--strip",
        dest="strip",
        action="store_true",
        help="ignore the white spaces",
        )
    parser.add_argument(
        "folder",
        metavar="FOLDER",
        nargs="?",
        default=".",
        help="the given folder or file.",
        )
    return parser, parser.parse_args()

def FEndswith(fpath, search, strip):
        fsize = os.stat(fpath).st_size
        with open(fpath, "rb") as fobj:
            if fsize > 1024:
                fobj.seek(-1024, 2)
            
            buf = fobj.read()
            if strip:
                buf = buf.rstrip()
            
            if buf.endswith(search):
                print(fpath)

def Main():
    parser, opt = ParseCommandLine()
    
    search = unescape(opt.search.encode(opt.encoding))
    folder = os.path.realpath( opt.folder )
    
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for f in files:
                ff = os.path.join(root, f)
                FEndswith(ff, search, opt.strip)
    elif os.path.isfile(folder):
        FEndswith(folder, search, opt.strip)
    else:
        os.sys.exit(1)
    
if __name__ == '__main__':
    Main()



