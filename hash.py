# encoding: utf-8
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
        description = "计算文件内容的HASH值。默认从标准输入中获取文件内容。",
        epilog = EPILOG,
        )
    parser.add_argument(
        "file",
        nargs="*",
        default=["-"],
        help="文件。“-”表示从标准输入中获取内容。",
        )
    
    if not hashmethodname:
        parser.add_argument(
            "-m", "--method",
            dest="method",
            action="store",
            required=True,
            choices=METHOD_CHOICES,
            help="HASH算法。可选的有：md5/sha1/sha224/sha256/sha384/sha512。",
            )
    
    return parser, parser.parse_args()

def Main():
    global hashmethodname
    
    parser, opt = ParseCommandLine()
    
    if not hashmethodname:
        hashmethodname = opt.method
    
    hashmethodname = hashmethodname.strip().lower()
    hashmethod = getattr(hashlib, hashmethodname, None)
    
    if not hashmethod:
        parser.print_usage()
        print("error: unimplemented hash method [%s]..."%(hashmethodname))
        os.sys.exit(1)
        
    files = []
    for f in opt.file:
        
        if f == "-":
            fobj = os.sys.stdin.buffer
        else:
            fobj = open(f, "rb")
        
        m = hashmethod()
        while True:
            t = fobj.read(1024)
            if t:
                m.update(t)
            else:
                break
        
        if f != "-":
            fobj.close()
        
        print( "%s %s %s"%(hashmethodname, m.hexdigest(), f) )
        
if __name__ == '__main__':
    Main()