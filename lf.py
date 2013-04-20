# encoding: utf-8
"""
just for example:

    #
    # line number a file
    #
    type lf.py | lf -n
    
    #
    # find all function definition lines
    #
    D:\Projects\pytools>type lf.py | lf -n -c "^\W*def\W+.*\W*\(.*\)\W*:"
       51 def ParseCommandLine():
      103 def Main():
    
    #
    # find all function names
    #
    D:\Projects\pytools>type lf.py | lf -s "def\W*(.*)\W*\("  -c "^\W*def\W+.*\W*\(.*\)\W*:"
    ParseCommandLine
    Main
    
    #
    # 提取ping值的延迟时间
    #
    D:\Projects\pytools>ping www.baidu.com
    
    正在 Ping www.a.shifen.com [220.181.111.147] 具有 32 字节的数据:
    来自 220.181.111.147 的回复: 字节=32 时间=59ms TTL=54
    来自 220.181.111.147 的回复: 字节=32 时间=60ms TTL=54
    来自 220.181.111.147 的回复: 字节=32 时间=58ms TTL=54
    来自 220.181.111.147 的回复: 字节=32 时间=60ms TTL=54
    
    220.181.111.147 的 Ping 统计信息:
        数据包: 已发送 = 4，已接收 = 4，丢失 = 0 (0% 丢失)，
    往返行程的估计时间(以毫秒为单位):
        最短 = 58ms，最长 = 60ms，平均 = 59ms
    
    D:\Projects\pytools>ping www.baidu.com | python lf.py -e gb18030 -c "TTL=" -s "时间=(.*)ms\W+"
    58
    60
    60
    58
"""
import os
import re
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="line string filter. use re-pattern as filter condition. allow multi-conditions.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        default="utf-8",
        help="set the file encoding or else treat as utf-8",
        )
    parser.add_argument(
        "-r", "--or",
        dest="cor",
        action="store_true",
        help="use OR to connect the conditions or else use AND",
        )
    parser.add_argument(
        "-c", "--conditions",
        dest="cond",
        action="store",
        nargs="+",
        default=[],
        help="re-patterned filter conditions. can be used multi-times",
        )
    parser.add_argument(
        "-d", "--delete",
        dest="delete",
        action="store_true",
        help="delete the lines match the filter"
        )
    parser.add_argument(
        "-s", "--sub",
        dest="sub",
        action="store",
        help="print substring of the line. use re-pattern. print out the re-find result."
        )
    parser.add_argument(
        "-n", "--line-number",
        dest="lineno",
        action="store_true",
        help="show line numbers",
        )
    parser.add_argument(
        "file",
        nargs="?",
        default=["-"],
        help="target file. use - for stdin"
    )
    return parser, parser.parse_args()

def Main():
    parse, opt = ParseCommandLine()
    
    filepath= opt.file[0]
    if filepath == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = open(filepath, "rb")
    
    lineno = 0
    conds = [c.encode(opt.encoding) for c in opt.cond]
    while 1:
        lineno += 1
        
        line = fileobj.readline()
        if not line:
            break
        
        if opt.cor:
            lineflag = False
        else:
            lineflag = True
        
        for cond in conds:
            flag = False
            if re.findall(cond, line):
                flag = True
                
            if flag and opt.cor:
                lineflag = True
                break
            elif not flag and not opt.cor:
                lineflag = False
                break
        
        if opt.sub:
            subpattern = opt.sub.encode(opt.encoding)
        else:
            subpattern = b""
            
        if (lineflag and not opt.delete) or (not lineflag and opt.delete):
            
            if opt.lineno:
                os.sys.stdout.buffer.write( ("%5d "%(lineno)).encode("ascii") )
                
            if subpattern:
                rs = re.findall(subpattern, line)
                os.sys.stdout.buffer.write(b" ".join(rs)+os.linesep.encode("ascii"))
            else:
                os.sys.stdout.buffer.write(line)
    
if __name__ == '__main__':
    Main()