# encoding: utf-8
import os
import argparse
from inc import epilog

def ArgParse():
    parser = argparse.ArgumentParser(
        description="Concatenate FILE(s), or standard input, to standard output.",
        epilog=epilog
        )
    parser.add_argument(
        "-A", "--show-all",
        dest="show_all",
        action="store_true",
        help="equivalent to -vET",
        )
    parser.add_argument(
        "-b", "--number-nonblank",
        dest="number_nonblank",
        action="store_true",
        help="number nonempty output lines",
        )
    parser.add_argument(
        "-B", "--number-lines",
        dest="number_lines",
        action="store_true",
        help="number output lines",
        )    
    parser.add_argument(
        "-e",
        dest="show_ends2",
        action="store_true",
        help="equivalent to -vE",
        )
    parser.add_argument(
        "-E", "--show-ends",
        dest="show_ends",
        action="store_true",
        help="display $ at end of each line",
        )
    parser.add_argument(
        "-s", "--squeeze-blank",
        dest="squeeze_blank",
        action="store_true",
        help="suppress repeated empty output lines",
        )
    parser.add_argument(
        "-t",
        dest="show_tabs2",
        action="store_true",
        help="equivalent to -vT",
        )
    parser.add_argument(
        "-T", "--show-tabs",
        dest="show_tabs",
        action="store_true",
        help="display TAB characters as ^I",
        )
    parser.add_argument(
        "-v", "--show-nonprinting",
        dest="show_nonprinting",
        action="store_true",
        help="use ^ and M- notation, except for LFD and TAB",
        )
    parser.add_argument(
        "file",
        nargs="*",
        default=["-"],
        )
    args = parser.parse_args()
    return parser, args

def Main():
    parser, args = ArgParse()
        
    print(parser)
    print(args)

if __name__ == '__main__':
    Main()