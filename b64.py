# encoding: utf-8
import os
import base64
import argparse
from inc import EPILOG

def StringChunk(s, size):
    for i in range(0, len(s), size):
        yield s[ i: i+size ]
        
def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "BASE64编解码工具。",
        epilog = EPILOG,
        )
    parser.add_argument(
        "-d", "--decode",
        dest="decode",
        action="store_true",
        help="进行解码操作。",
        )
    parser.add_argument(
        "-b", "--linebreak",
        dest="linebreak",
        action="store_true",
        help="每76字符换行。URL SAFE编码时无效。解码时无效。",
        )
    parser.add_argument(
        "-u", "--url-safe",
        dest="url_safe",
        action="store_true",
        help="URL SAFE标识。",
        )
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        help="目标文件。使用“-”表示从标准输入读取",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    if opt.file == "-":
        content = os.sys.stdin.buffer.raw.read()
    else:
        with open(opt.file, "rb") as f:
            content = f.read()
    
    if opt.url_safe:
        if opt.decode:
            content2 = base64.urlsafe_b64decode(content)
        else:
            content2 = base64.urlsafe_b64encode(content)
    else:
        if opt.decode:
            content2 = base64.decodestring(content)
        else:
            content2 = base64.encodestring(content)
    
    if not opt.decode:
        content2 = content2.replace(b"\r", b"").replace(b"\n", b"")
        if opt.linebreak and not opt.url_safe:
            cs = list(StringChunk(content2, 76))
            content2 = b"\n".join(cs)
    
    os.sys.stdout.buffer.raw.write(content2)
    os.sys.stdout.buffer.raw.flush()
    
if __name__ == '__main__':
    Main()













