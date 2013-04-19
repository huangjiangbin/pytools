import os
import hashlib
import argparse
from inc import EPILOG
from func import GetProgramPath

METHOD_CHOICES = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]

prog = GetProgramPath()
try:
    progname = os.path.splitext( os.path.split(prog)[1] )[0]
except:
    progname = ""
hashmethodname = ""
if progname in METHOD_CHOICES:
    hashmethodname = progname
    
def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "Print hash result. With no FILE or when FILE is -, read from standard input.",
        epilog = epilog
        )
    parser.add_argument(
        "file",
        nargs="*",
        default=["-"],
        )
    
    if not hashmethodname:
        parser.add_argument(
            "-m", "--method",
            dest="method",
            action="store",
            required=True,
            choices=METHOD_CHOICES,
            help="hash method. md5/sha1/sha224/sha256/sha384/sha512.",
            )
    
    return parser, parser.parse_args()

def Main():
    global hashmethodname
    
    parser, opt = ParseCommandLine()
    
    if not hashmethodname:
        hashmethodname = opt.method
    
    hashmethodname = hashmethodname.strip()
    hashmethod = getattr(hashlib, hashmethodname, None)
    
    if not hashmethod:
        parser.print_usage()
        print("error: unimplemented hash method [%s]..."%(hashmethodname))
        os.sys.exit(1)
        
    files = []
    for f in opt.file:
        fromstdin = False
        if f == "-":
            fobj = os.sys.stdin.buffer
            fromstdin = True
        else:
            fobj = open(f, "rb")
        
        m = hashmethod()
        while 1:
            t = fobj.read(524288)
            if t:
                m.update(t)
            else:
                break
        
        if not fromstdin:
            fobj.close()
        
        print( "%s %s %s"%(hashmethodname, m.hexdigest(), f) )
        
if __name__ == '__main__':
    Main()