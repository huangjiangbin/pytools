import os
import re
import argparse
from inc import EPILOG

BUFFER_SIZE = 1024*32-1

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Replace file content line by line. If the FILE is stdin, output to stdout, or else write the result back to the content file.",
        epilog=EPILOG
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        default="utf-8",
        help="content encoding. default utf-8.",
        )
    parser.add_argument(
        "-i", "--ignore-case",
        dest="ignorecase",
        action="store_true",
        default=False,
        help="ignore character case while searching.",
        )
    parser.add_argument(
        "-s", "--search",
        dest="search",
        action="store",
        required=True,
        help="re.sub(...) search pattern",
        )
    parser.add_argument(
        "-r", "--replace",
        dest="replace",
        action="store",
        required=True,
        help="re.sub(...) repl content",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="content file. use - for stdin."
        )
    return parser, parser.parse_args()

class ReplaceCallback:
    def __init__(self, formatter):
        self.formatter = formatter
    
    def __call__(self, m):
        return self.formatter.format(*m.groups())
    
def Main():
    parser, opt = ParseCommandLine()
    
    reflags = 0
    if opt.ignorecase:
        reflags |= re.IGNORECASE
    
    if opt.file == "-":
        fin = os.sys.stdin
        fout = os.sys.stdout
    else:
        fin = open(opt.file, "rt", encoding=opt.encoding)
        
        finpath = os.path.realpath(opt.file)
        fdir, fname = os.path.split(finpath)
        foutname = "."+fname+".swp"
        foutpath = os.path.join(fdir, foutname)
        fout = open(foutpath, "wt", encoding=opt.encoding)
    
    if re.findall( "{.*}", opt.replace ):
        use_callback = True
        resub_callback = ReplaceCallback(opt.replace)
    else:
        use_callback = False
    
    while 1:
        buf = fin.readline()
        if not buf:
            break
        
        if use_callback:
            r = re.sub(opt.search, resub_callback, buf, flags=reflags)
        else:
            r = re.sub(opt.search, opt.replace, buf, flags=reflags)
        
        fout.write(r)

    if opt.file != "-":
        fin.close()
        fout.close()
        
        ftmpath = os.path.join(fdir, "."+fname+".tmp")
        if os.path.isfile(ftmpath):
            os.unlink(ftmpath)
        os.rename(finpath, ftmpath)
        os.rename(foutpath, finpath)
        os.unlink(ftmpath)

if __name__ == '__main__':
    Main()