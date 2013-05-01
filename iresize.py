import os
from PIL import Image
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="resize image file. the source image file will be replaced.",
        epilog=EPILOG,
        conflict_handler="resolve",
        )
    parser.add_argument(
        "-w", "--width",
        dest="width",
        action="store",
        type=int,
        default=0,
        help="target image width",
        )
    parser.add_argument(
        "-h", "--height",
        dest="height",
        action="store",
        type=int,
        default=0,
        help="target image height"
        )
    parser.add_argument(
        "-s", "--smart",
        dest="smart",
        action="store_true",
        help="auto crop to fit the target size. only available while both width and height are given.",
        )
    parser.add_argument(
        "-p", "--position",
        dest="pos",
        action="store",
        choices=["left", "right", "center"],
        default="center",
        help="crop position. default to center. left also means top, and right also means bottom.",
    )
    parser.add_argument(
        "file",
        metavar="IMAGE_FILE",
        nargs=1,
        help="source image file",
        )
    return parser, parser.parse_args()

def GetCropBox( source_width, source_height, target_width, target_height, pos):
    dw = (source_width - target_width ) / 2
    dh = (source_height - target_height ) / 2
    if pos == "left":
        return (
                0,
                0,
                target_width,
                target_height,
            )
    elif pos == "right":
        return (
                source_width-target_width,
                source_height-target_height,
                source_width,
                source_height,
            )
    else:
        return (
                int(dw),
                int(dh),
                int(dw+target_width),
                int(dh+target_height),
            )
def Main():
    parser, opt = ParseCommandLine()
    
    if opt.width == 0 and opt.height == 0:
        print("you must give at least width or height.")
        os.sys.exit(1)
    
    target_width = opt.width
    target_height = opt.height
    
    imagefile = opt.file[0]
    if not os.path.isfile(imagefile):
        print("%s is not a file."%(imagefile))
        os.sys.exit(2)
    
    imagefile = os.path.realpath(imagefile)
    imagedir, imagename = os.path.split(imagefile)
    iname, iext = os.path.splitext(imagename)
    swpfile = os.path.join(imagedir, "."+iname+".swp"+iext)
    tmpfile = os.path.join(imagedir, "."+iname+".tmp"+iext)
    
    try:
        source = Image.open(imagefile)
    except:
        print("%s is not an image file."%(imagefile))
        os.sys.exit(3)
    
    source_width, source_height = source.size
    if target_width and target_height == 0:
        target_height = int( source_height * target_width / source_width ) + 1
    elif target_height and target_width == 0:
        target_width = int( source_width * target_height / source_height ) + 1
    
    if opt.smart and (source_width * target_height > source_height * target_width):
        tmp_height = target_height
        tmp_width = int( source_width * tmp_height / source_height ) + 1
        crop_box = GetCropBox(tmp_width, tmp_height, target_width, target_height, opt.pos)
        source.thumbnail( (tmp_width, tmp_height) )
        source = source.crop(crop_box)
        source.save(swpfile)
    elif opt.smart and (source_width * target_height < source_height * target_width):
        tmp_width = target_width
        tmp_height = int( source_height * tmp_width / source_width ) + 1
        crop_box = GetCropBox(tmp_width, tmp_height, target_width, target_height, opt.pos)
        source.thumbnail( (tmp_width, tmp_height) )
        source = source.crop(crop_box)
        source.save(swpfile)
    else:    
        source.thumbnail( (target_width, target_height) )
        source.save(swpfile)
    
    if os.path.isfile(tmpfile):
        os.unlink(tmpfile)
    os.rename(imagefile, tmpfile)
    os.rename(swpfile, imagefile)
    os.unlink(tmpfile)
    
if __name__ == '__main__':
    Main()








