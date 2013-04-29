import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="find absolute path of a command",
        epilog=EPILOG,
        )
    parser.add_argument(
        "command",
        metavar="COMMAND",
        nargs=1,
        help="command name",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    command = opt.command[0].lower()
    targets = []
    
    paths = os.environ.get("PATH").split(";")
    for path in paths:
        try:
            files = os.listdir(path)
        except:
            files = []
                
        for f in files:
            name, ext = os.path.splitext(f)
            if (f.lower() == command) or (name.lower() == command):
                targets.append(
                    (path, name, ext)
                )
    
    if not targets:
        os.sys.exit(1)
    
    exts = [x.lower() for x in os.environ.get("PATHEXT").split(";")]
    
    targets[0]
    for t in targets:
        if t[2].lower() in exts:
            target = t
            break
    
    print(os.path.abspath("%s/%s%s"%(target[0], target[1], target[2])))

if __name__ == '__main__':
    Main()