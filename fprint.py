# encoding: utf-8
import os
import argparse
from inc import EPILOG
from func import StdoutWrite

def ArgParse():
    parser = argparse.ArgumentParser(
        description="打印文件内容到标准输出上。不指定输入文件，则从标准输入读取内容。",
        epilog=EPILOG
        )
    parser.add_argument(
        "-n", "--number-lines",
        dest="show_line_number",
        action="store_true",
        help="显示行号",
        )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        default=["-"],
        help="输入文件",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ArgParse()
    
    for f in opt.files:
        
        if f == "-":
            fileobj = os.sys.stdin.buffer.raw
        else:
            fileobj = open(f, "rb")
        
        line_number = 0
        
        line = b""
        lastline = b""
        while True:
            line_number += 1
            line = fileobj.readline()
            if not line:
                break
            
            if opt.show_line_number:
                line = ( "%4d "%(line_number) ).encode( "ascii" ) + line
            
            StdoutWrite(line)
            lastline = line
        
        if not ( lastline.endswith( b"\n" ) or lastline.endswith( b"\r" ) ):
            print( "" )
            
        if f != "-":
            fileobj.close()

if __name__ == '__main__':
    Main()
    
    