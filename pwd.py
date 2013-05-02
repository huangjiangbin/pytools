import os
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="show current directory path",
        epilog=EPILOG,
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    print( os.getcwd() )

if __name__ == '__main__':
    Main()