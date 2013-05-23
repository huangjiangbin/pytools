# encoding: utf-8
import re
import time
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "休眠指定时间后返回。",
        epilog = EPILOG,
        )
    parser.add_argument(
        "-m", "--millisecond",
        dest="millisecond",
        action="store_true",
        help="以毫秒为单位。"
        )
    parser.add_argument(
        "n",
        nargs=1,
        type=int,
        help="指定休眠的时间。默认单位为秒，如使用了-m选项，则单位为毫秒。",
        )
    parser.add_argument(
        "-i", "--information",
        dest="information",
        action="store",
        help="在休眠前，显示提示信息。如需要换行，则使用<br />代替。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    sleeptime = opt.n[0]
    if opt.millisecond:
        sleeptime /= 1000.0
    
    opt.information = re.sub("<br[^<>]*>", "\r\n", opt.information)
    if opt.information:
        print(opt.information, end="", flush=True)
    
    try:
        time.sleep(sleeptime)
    except KeyboardInterrupt:
        pass
    
if __name__ == '__main__':
    Main()