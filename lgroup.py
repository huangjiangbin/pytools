# encoding: utf-8
import os
import re
import io
import argparse
import subprocess

from inc import EPILOG
from func import StdoutWrite

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="按行里的元信息分组。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="meta_encoding",
        action="store",
        default="utf-8",
        help="元信息提取规则编码。",
        )
    parser.add_argument(
        "-s", "--group-separator",
        dest="group_separator",
        action="store",
        default="#"*50,
        help="组分隔符。默认为50个“#”。",
        )
    parser.add_argument(
        "-m", "--meta",
        dest="meta",
        action="store",
        required=True,
        help="元信息提取规则。支持正则。",
        )
    parser.add_argument(
        "-N", "--print-no-match-lines",
        dest="print_no_match_lines",
        action="store_true",
        help="显示不匹配行。",
        )
    parser.add_argument(
        "-c", "--command",
        dest="command",
        action="store",
        help="动作。对每个分组执行指定命令。该命令应该从标准输入中读取分组内容。",
        )
    parser.add_argument(
        "-f", "--file",
        dest="file",
        action="store",
        default="-",
        help="目标文件。默认为“-”，表示从标准输入中读取内容。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = open(opt.file, "rb")
    
    data0 = []
    data = {}
    rep = re.compile( opt.meta.encode( opt.meta_encoding ) )
    group_separator = opt.group_separator.encode( opt.meta_encoding )
    linesep = b"\n"
    
    while True:
        line = fileobj.readline()
        if not line:
            break
        
        if linesep == b"\n":
            if b"\r" in line:
                linesep = b"\r\n"
        
        if not (line.endswith(b"\n") or line.endswith(b"\r")):
            line += linesep
        
        m = rep.match(line)
        if not m:
            data0.append( line )
        else:
            key = m.groups()
            if not key in data:
                data[ key ] = []
            data[ key ].append( line )
    
    group_separator += linesep
    
    keys = list(data.keys())
    keys.sort()
    for key in keys:
        lines = data[key]
        if not opt.command:
            StdoutWrite(b"".join(lines))
            StdoutWrite(group_separator)
        else:
            proc = subprocess.Popen( opt.command, stdin=subprocess.PIPE, shell=True)
            proc.communicate(b"".join(lines))
            proc.wait()
            
    if opt.print_no_match_lines:
        if not opt.command:
            StdoutWrite(b"".join(data0))
            StdoutWrite(group_separator)
        else:
            proc = subprocess.Popen( opt.command, stdin=subprocess.PIPE, shell=True)
            proc.communicate(b"".join(data0))
            proc.wait()
        
    if opt.file != "-":
        fileobj.close()
    
if __name__ == '__main__':
    Main()
