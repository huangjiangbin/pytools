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
        if f == "-":
            fobj = os.sys.stdin.buffer
        else:
            try:
                fobj = open(f, "rb")
            except Exception as e:
                fobj = None
                
        if fobj:
            m = hashlib.md5()
            while 1:
                t = fobj.read(524288)
                if t:
                    m.update(t)
                else:
                    break
            a = m.hexdigest()
        else:
            a = "-"
        print( "%s: %s"%(a, f) )

if __name__ == '__main__':
    Main()