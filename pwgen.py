import os
import time
import random
import string
import argparse
from inc import epilog

random.seed(time.time())

def PWGen(opt):
    s = ""
    s += string.ascii_letters
    if not opt.without_digits:
        s += string.digits * 3
    if opt.with_symbols:
        s += string.punctuation
    
    s = list(s)
    n = int(opt.length / len(s))
    if n > 0:
        s *= (n+1)
        
    for x in range( 0, random.randint(100,200) ):
        random.shuffle(s)
    return "".join( s[:opt.length] )

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="random password generator",
        epilog=epilog,
        )
    parser.add_argument(
        "-l", "--length",
        dest="length",
        default=8,        
        type=int,
        help="password length",
        )
    parser.add_argument(
        "-n", "--without-digits",
        dest="without_digits",
        action="store_true",
        help="do NOT use digits",
    )
    parser.add_argument(
        "-s", "--with-symbols",
        dest="with_symbols",
        action="store_true",
        help="use symbol characters",
        default=False,
        )
    args = parser.parse_args()
    return parser, args

def Main():
    parser, opt = ParseCommandLine()
    print(PWGen(opt))
    
if __name__ == '__main__':
    Main()