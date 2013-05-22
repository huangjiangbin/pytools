# encoding: utf-8
import os
from urllib.request import urlopen
import argparse
from inc import EPILOG

def _smart_unicode(s):
    try:
        return s.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return s.decode("gb18030")
        except UnicodeDecodeError:
            try:
                return s.decode("ISO-8859-1")
            except UnicodeDecodeError:
                return ""

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="URL下载工具。",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        action="store",
        default="-",
        help="将内容保存至该文件中。如果不指定或指定为“-”，将下载内容输出到控制台屏幕上。",
        )
    parser.add_argument(
        "-u", "--unicode",
        dest="unicode",
        action="store_true",
        help="将下载内容当作是unicode字符串。",
        )
    parser.add_argument(
        "url",
        metavar="URL",
        nargs=1,
        help="目标URL地址。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    target_url = opt.url[0]
    
    if opt.output == "-":
        t = urlopen(target_url).read()
        
        if opt.unicode:
            t = _smart_unicode(t)
            print(t)
        else:
            os.sys.stdout.buffer.write(t)
            os.sys.stdout.flush()
    else:
        r = urlopen(target_url)
        with open(opt.output, "wb") as fileobj:
            while True:
                t = r.read(1024*16)
                if not t:
                    break
                fileobj.write(t)
                print(".", end="", flush=True)
        print("File saved to %s"%(os.path.realpath(opt.output)))
        
if __name__ == '__main__':
    Main()
