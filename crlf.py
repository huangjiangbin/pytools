import os
import argparse
from inc import EPILOG

BUFFER_SIZE = 1024*32-1

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="change the line breaker to windows/linux/macos style",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-r",
        dest="r",
        action="store_true",
        help="add \\r in line break",
        )
    parser.add_argument(
        "-n",
        dest="n",
        action="store_true",
        help="add \\n in line break"
        )
    parser.add_argument(
        "f",
        nargs="?",
        default="-",
        help="target file, if not provide or use - for stdin",
        )
    return parser, parser.parse_args()


def Main():
    parser, opt = ParseCommandLine()
    
    if (not opt.r and not opt.n) or (opt.r and opt.n):
        opt.r = True
        opt.n = True
        end = b"\r\n"
    elif opt.r:
        end = b"\r"
    elif opt.n:
        end = b"\n"
    else:
        end = b""
        
    if opt.f == "-":
        cin = os.sys.stdin.buffer
        cout = os.sys.stdout.buffer
    else:
        fname = os.path.split(opt.f)[1]
        fdir = os.path.dirname(os.path.realpath(opt.f))
        fin = os.path.join(fdir, fname)
        fout = os.path.join(fdir, "."+fname+".swp")
        
        cin = open(opt.f, "rb")
        cout = open(fout, "wb")
    
    while 1:
        line = cin.read(BUFFER_SIZE)
        if not line:
            break
        
        linesize = len(line)
        idx = 0
        nflag = False
        while idx < linesize:
            c = line[idx:idx+1]
            if c == b"\r":
                cout.write(end)
                nflag = True
            elif c == b"\n":
                if nflag:
                    nflag = False
                else:
                    cout.write(end)
            else:
                cout.write(c)
            
            idx += 1
    
    if opt.f != "-":
        cin.close()
        cout.close()
        
        ftmp = os.path.join(fdir, "."+fname+".tmp")
        if os.path.isfile(ftmp):
            os.unlink(ftmp)
            
        os.rename(fin, ftmp)
        os.rename(fout, fin)
        os.unlink(ftmp)
        
if __name__ == '__main__':
    Main()