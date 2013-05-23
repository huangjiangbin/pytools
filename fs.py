# encoding: utf-8
import os
import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser( 
        description="列举目录下的文件或子目录。",
        epilog=EPILOG,
        )
    parser.add_argument( 
        "-R", "--relative",
        dest="relative",
        action="store_true",
        help="显示相对路径。",
        )
    parser.add_argument( 
        "-r", "--recursive",
        dest="recursive",
        action="store_true",
        help="递归处理所有子目录。",
        )
    parser.add_argument( 
        "-d", "--show-directories",
        dest="show_dir",
        action="store_true",
        help="只显示目录。指定-a后，本选项无效。",
        )
    parser.add_argument( 
        "-a", "--show-all",
        dest="show_all",
        action="store_true",
        help="显示目录和文件。",
        )
    parser.add_argument( 
        "folder",
        metavar="FOLDER",
        nargs="?",
        default=".",
        help="根目录。",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    folder = os.path.realpath( opt.folder )
    if not opt.recursive:
        fs = os.listdir( folder )
        
        if opt.show_all or opt.show_dir:
            for f in fs:
                ff = os.path.realpath( os.path.join( folder, f ) )
                if os.path.isdir( ff ):
                    if opt.relative:
                        print( f+os.path.sep )
                    else:
                        print( ff+os.path.sep )
        
        if opt.show_all or ( not opt.show_dir ):
            for f in fs:
                ff = os.path.realpath( os.path.join( folder, f ) )
                if os.path.isfile( ff ):
                    if opt.relative:
                        print( f )
                    else:
                        print( ff )
    else:
        for root, dirs, files in os.walk( folder ):
            
            if opt.show_all or opt.show_dir:
                if opt.relative:
                    print( root[len( folder )+1:]+os.path.sep )
                else:
                    print( root+os.path.sep )
            
            if opt.show_all or (not opt.show_dir):
                for f in files:
                    ff = os.path.realpath( os.path.join( root, f ) )
                    if opt.relative:
                        print( ff[len( folder )+1:] )
                    else:
                        print( ff )
    

if __name__ == '__main__':
    Main()




