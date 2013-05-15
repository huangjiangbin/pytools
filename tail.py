import os
import argparse
from inc import EPILOG

BUFSIZE = 1024*1024*16

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Show the tail lines of a file.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-f", "--file",
        dest="file",
        action="store",
        default="-",
        help="Target file.",
        )
    parser.add_argument(
        "-n", "--number",
        dest="number",
        action="store",
        type=int,
        default=0,
        help="Show last N lines.",
        )
    return parser, parser.parse_args()

def Main():
    paser, opt = ParseCommandLine()
    
    if opt.file == "-":
        fileobj = os.sys.stdin.buffer
    else:
        fileobj = os.open(opt.file, os.O_RDONLY)
    
    if opt.number:
        if opt.file == "-":
            lines = fileobj.readlines()
            for line in lines[ len(lines)-opt.number : ]:
                os.sys.stdout.buffer.write(line)
        else:
            if os.stat(opt.file).st_size > BUFSIZE:
                fileobj.seek(-1*BUFSIZE, 2)
            buf = os.read( fileobj, BUFSIZE )
            lines = buf.splitlines()
            for line in lines[ len(lines)-opt.number : ]:
                os.sys.stdout.buffer.write(line+b"\r\n")
        os.sys.stdout.buffer.flush()
    else:
        # wait for another process write to the file
        # not ready...
        pass
    
    if opt.file != "-":
        os.close(fileobj)
        
if __name__ == '__main__':
    Main()
