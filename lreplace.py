# encoding: utf-8
import os
import re
import argparse
from inc import EPILOG

BUFFER_SIZE = 1024*32-1

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="文件内容替换工具。支持正则匹配。",
        epilog=EPILOG
        )
    parser.add_argument(
        "-i", "--ignore-case",
        dest="ignorecase",
        action="store_true",
        default=False,
        help="忽略大小写。",
        )
    parser.add_argument(
        "-s", "--search",
        dest="search",
        action="store",
        required=True,
        help="查询规则。支持正则和正则组。",
        )
    parser.add_argument(
        "-r", "--replace",
        dest="replace",
        action="store",
        required=True,
        help="替换字符串。使用\\1, \\2, ... \\n代替正则组。",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="目标文件。默认为“-”表示从标准输入中读取。"
        )
    return parser, parser.parse_args()

class ReplaceCallback:
    def __init__(self, formatter):
        self.formatter = formatter
    
    def __call__(self, m):
        return self.formatter.format(*m.groups())
    
def Main():
    parser, opt = ParseCommandLine()
    
    reflags = re.M
    if opt.ignorecase:
        reflags |= re.I
    
    if opt.file == "-":
        fin = os.sys.stdin.buffer.raw
        fout = os.sys.stdout.buffer.raw
    else:
        fin = open(opt.file, "rb")
        
        finpath = os.path.realpath(opt.file)
        fdir, fname = os.path.split(finpath)
        foutname = "."+fname+".swp"
        foutpath = os.path.join(fdir, foutname)
        fout = open(foutpath, "w")
    
    content = fin.read()
    
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