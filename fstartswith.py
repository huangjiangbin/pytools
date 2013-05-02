import os
import re
import argparse
from inc import EPILOG

def unescape(buf):
    buf = buf.replace(b"\\\\", b"guess_unused_20130502")
    
    def f1(x):
        cs = {
            b"n": b"\n",
            b"t": b"\t",
            b"v": b"\v",
            b"b": b"\b",
            b"r": b"\r",
            b"f": b"\f",
            b"a": b"\a",
        }
        c = x.groups()[0]
        return cs.get(c, b"")
    
    def f2(x):
        c = x.groups()[0]
        return chr( int(c.decode("utf-8")) ).encode("utf-8")
    
    def f3(x):
        c = x.groups()[0]
        return chr( int(c.decode("utf-8"), 16) ).encode("utf-8")
    
    buf = re.sub(b"\\\\([ntvbrfa])", f1, buf)
    buf = re.sub(b"\\\\([0-9]{3})", f2, buf)
    buf = re.sub(b"\\\\[xX]([0-9a-fA-F]{2})", f3, buf)
    
    return buf.replace(b"guess_unused_20130502", b"\\")

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="find files startswith given string",
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

def FStartswith(fpath, search, strip):
    try:
        with open(fpath, "rb") as fobj:
            buf = fobj.read(1024)
            if strip:
                buf = buf.lstrip()
            
            if buf.startswith(search):
                print(fpath)
    except:
        pass
    
def Main():
    parser, opt = ParseCommandLine()
    
    search = unescape(opt.search.encode(opt.encoding))
    folder = os.path.realpath( opt.folder )
    
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for f in files:
                ff = os.path.join(root, f)
                FStartswith(ff, search, opt.strip)
    elif os.path.isfile(folder):
        FStartswith(folder, search, opt.strip)
    else:
        os.sys.exit(1)
        
if __name__ == '__main__':
    Main()



