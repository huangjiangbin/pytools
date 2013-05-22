# encoding: utf-8
import os
import argparse
from inc import EPILOG
from func import StripCRLF

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="显示指定列。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        default="utf-8",
        help="文件编码。",
        )
    parser.add_argument(
        "-n", "--number",
        dest="number",
        action="store",
        required=True,
        help="指定列。允许指定多列，使用逗号分隔。",
        )
    parser.add_argument(
        "-d", "--delimiter",
        dest="delimiter",
        action="store",
        default=" ",
        help="如果指定多列，输出时的分隔符。默认为一个空格。",
        )
    parser.add_argument(
        "-s", "--separator",
        dest="separator",
        action="store",
        default="",
        help="目标文件的分隔符。",
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default="-",
        help="目标文件。使用“-”表示从标准输入读取文件。",
    )
    return parser, parser.parse_args()

def Main():
    paser, opt = ParseCommandLine()
    
    separator = opt.separator.encode(opt.encoding)
    delimiter = opt.delimiter.encode(opt.encoding)
    numbers = [ int(x.strip()) for x in opt.number.split(",") ]
    
    if opt.file == "-":
        lines = os.sys.stdin.buffer.readlines()
    else:
        with open(opt.file, "rb") as fileobj:
            lines = fileobj.readlines()
    
    for line in lines:
        line = StripCRLF(line)
        if not separator:
            ss = line.split()
        else:
            ss = line.split(separator)
        
        ts = []
        for n in numbers:
            if n == 0:
                ts.append( line )
            else:
                if n <= len(ss):
                    ts.append( ss[n-1] )
        
        str_line = delimiter.join(ts)
        os.sys.stdout.buffer.write(str_line+b"\r\n")
        os.sys.stdout.buffer.flush()
    
if __name__ == '__main__':
    Main()
