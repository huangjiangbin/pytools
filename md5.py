import os
import hashlib
import argparse
from inc import epilog


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "Print or check MD5 (128-bit) checksums. With no FILE, or when FILE is -, read standard input.",
        epilog = epilog
        )
    parser.add_argument(
        "file",
        nargs="*",
        default=["-"],
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    files = []
    for f in opt.file:
        fromstdin = False
        if f == "-":
            fobj = os.sys.stdin.buffer
            fromstdin = True
        else:
            fobj = open(f, "rb")
        
        m = hashlib.md5()
        while 1:
            t = fobj.read(524288)
            if t:
                m.update(t)
            else:
                break
        
        if not fromstdin:
            fobj.close()
        
        print( "%s: %s"%(m.hexdigest(), f) )
        
if __name__ == '__main__':
    Main()