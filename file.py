import os
import magic
import argparse
from inc import EPILOG
from func import SmartUnicode, GetProgramPath

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Guess file type.",
        epilog=EPILOG,
        )
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs=1,
        help="Target file."
        )
    return parser, parser.parse_args()

def SearchMagicFile():
    progpath = GetProgramPath()
    prefix = os.path.dirname(progpath)
    
    files = [
            os.path.join(prefix, "magic.mgc"),
            os.path.join(prefix, "etc/magic.mgc"),
            os.path.join(prefix, "lib/magic.mgc"),
            os.path.join(prefix, "share/magic.mgc"),
        ]
    for f in files:
        if os.path.isfile( f ):
            return os.path.realpath( f )
    return ""

def Main():
    parser, opt = ParseCommandLine()
    filepath = opt.file[0]
    
    magic_file = SearchMagicFile()
    if not magic_file:
        print("magic.mgc file not found.")
        os.sys.exit(1)
        
    mobj = magic.Magic( magic_file = magic_file )
    info = mobj.from_file( filepath )
    print(SmartUnicode(info))


if __name__ == '__main__':
    Main()

    