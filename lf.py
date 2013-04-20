"""
just for example:
    type zipfile.py | lf -r -f - "^(\t*)class(.*):" "def "
        you get an overview of class&function definition of the python source code file
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
        "-r", "--or",
        dest="cor",
        action="store_true",
        help="use OR to connect the conditions or else use AND",
        )
    parser.add_argument(
        "-d", "--delete",
        dest="delete",
        action="store_true",
        help="delete the lines match the filter"
        )
    parser.add_argument(
        "cond",
        nargs="+",
        help="re-patterned filter condition",
        )
    parser.add_argument(
        "-f", "--file",
        dest="file",
        action="store",
        default="-",
        help="target file. use - for stdin"
    )
    return parser, parser.parse_args()

def Main():
    parse, opt = ParseCommandLine()
    
    if opt.file == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = open(opt.file, "rb")
    
    conds = [c.encode("utf-8") for c in opt.cond]
    while 1:
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
        
        if (lineflag and not opt.delete) or (not lineflag and opt.delete):
            os.sys.stdout.buffer.write(line)
    
if __name__ == '__main__':
    Main()