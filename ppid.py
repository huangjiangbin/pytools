import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="get current console's pid",
        epilog=EPILOG,
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    print( os.getppid() )

if __name__ == '__main__':
    Main()