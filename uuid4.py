import uuid
import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="uuid string generator",
        epilog=EPILOG,
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    print(str(uuid.uuid4()))

if __name__ == '__main__':
    Main()