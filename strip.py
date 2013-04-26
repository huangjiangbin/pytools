# encoding: utf-8
import os
import argparse
from inc import EPILOG

BUFFER_SIZE = 1024*32-1

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="remove blank chars at the beginning or at the end of the file",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-l", "--left",
        dest="left",
        action="store_true",
        help="remove blank chars at the beginning of the file"
        )
    parser.add_argument(
        "-r", "--right",
        dest="right",
        action="store_true",
        help="remove blank chars at the end of the file",
        )
    parser.add_argument(
        "-a", "--all",
        dest="all",
        action="store_true",
        help="remove blank chars both at the beginning and at the end of the file. if -a/--all provide, left/right are ignored"
        )
    parser.add_argument(
        "file",
        nargs="?",
        default=["-"],
        )
    args = parser.parse_args()
    return parser, args

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.all or (not opt.left and not opt.right):
        allflag = True
    else:
        allflag = False
    
    if allflag or opt.left:
        leftflag = True
    else:
        leftflag = False
        
    if allflag or opt.right:
        rightflag = True
    else:
        rightflag = False
    
    filepath = opt.file[0]
    if filepath == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = open(filepath, "rb")
    
    lastbuf = b''
    if leftflag:
        while 1:
            buf = fileobj.read1(BUFFER_SIZE)
            if not buf:
                break
            buf = buf.lstrip()
            if buf:
                lastbuf = buf
                break

    if not rightflag:
        if lastbuf:
            os.sys.stdout.buffer.write(lastbuf)
            lastbuf = b""
        
        while 1:
            buf = fileobj.read1(BUFFER_SIZE)
            if not buf:
                break
            os.sys.stdout.buffer.write(buf)
    else:
        while 1:
            buf = fileobj.read1(BUFFER_SIZE)
            if not buf:
                break
            
            if buf.strip():
                if lastbuf:
                    os.sys.stdout.buffer.write(lastbuf)
                lastbuf = buf
            else:
                lastbuf += buf
            
        if lastbuf:
            lastbuf = lastbuf.rstrip()
            if lastbuf:
                os.sys.stdout.buffer.write(lastbuf)
    
    os.sys.stdout.flush()
    
if __name__ == '__main__':
    Main()








