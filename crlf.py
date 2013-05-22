# encoding: utf-8
import os
import argparse
from inc import EPILOG

BUFFER_SIZE = 1024*32-1

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="更改换行符。Windows下常以\\r\\n为换行符；Linux下常以\\n为换行符；某些旧版的Mac OS以\\r为换行符。注意：目标文件将会被处理结果覆盖!!!",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-r",
        dest="r",
        action="store_true",
        help="将 \\r 加入到目标换行符中。",
        )
    parser.add_argument(
        "-n",
        dest="n",
        action="store_true",
        help="将 \\n 加入到目标换行符中。\\r和\\n都不出现时，将使用\\r\\n作为换行符。"
        )
    parser.add_argument(
        "f",
        nargs="?",
        default="-",
        help="目标文件。如果不指定目标文件或指定为“-”，将从标准输入中读取，并打印到标准输出。",
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