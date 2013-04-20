import os
import base64
import argparse
from inc import EPILOG

def StringChunk(s, size):
    for i in range(0, len(s), size):
        yield s[ i: i+size ]
        
def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "base64 encode/decode tools",
        epilog = EPILOG,
        )
    parser.add_argument(
        "-d", "--decode",
        dest="decode",
        action="store_true",
        help="decode the string",
        )
    parser.add_argument(
        "-b", "--linebreak",
        dest="linebreak",
        action="store_true",
        help="add line break every 76 characters while doing base64 encode(not urlsafe base64 encode)",
        )
    parser.add_argument(
        "-u", "--url-safe",
        dest="url_safe",
        action="store_true",
        help="url safe encode/docode",
        )
    parser.add_argument(
        "file",
        nargs="?",
        default=["-"],
        help="content file tobe encoded/decoded, - or not provided will use stdin",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    filepath = opt.file[0]
    if filepath == "-":
        content = os.sys.stdin.buffer.read()
    else:
        with open(filepath, "rb") as f:
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
    
    os.sys.stdout.buffer.write(content2)
    os.sys.stdout.flush()
    
if __name__ == '__main__':
    Main()













