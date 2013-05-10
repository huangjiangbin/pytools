


import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Find best main width for web grid design system.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-w", "--width",
        dest="width",
        action="store",
        default=1024,
        type=int,
        help="Screen size.",
        )
    parser.add_argument(
        "-d", "--delta",
        dest="delta",
        action="store",
        default=100,
        type=int,
        help="Choose result from [width-delta, width]. Default 100.",
        )
    parser.add_argument(
        "-p", "--padding",
        dest="padding",
        action="store",
        type=int,
        default=10,
        help="padding width.",
        )
    parser.add_argument(
        "columns",
        metavar="COLs",
        nargs="*",
        default=[1,2,3,4,5,6],
        help="Columns supported. Default to [1,2,3,4,5,6].",
        )
    return parser, parser.parse_args()

def GridTest(w, p):
    for n in range(1, 7):
        if ( w-p*(n-1) )%n != 0:
            return False
    return True

def Main():
    parser, opt = ParseCommandLine()
    
    widths = []
    wstart = opt.width-opt.delta
    if wstart < 1:
        wstart = 1
    columns = [ int(x) for x in opt.columns ]
    for w in range(wstart, opt.width+1):
        flag = True
        for n in columns:
            if ( w - opt.padding*(n-1) )%n != 0:
                flag = False
                break
        if flag:
            widths.append(w)

    print("    screen size: %d"%(opt.width))
    print("support columns: %s"%(", ".join([ str(x) for x in opt.columns])))
    print("  padding width: %d"%(opt.padding))
    print("     main width: %s"%(", ".join([ str(x) for x in widths ])))
    
if __name__ == '__main__':
    Main()
    