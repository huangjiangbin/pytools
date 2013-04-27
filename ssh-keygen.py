import os
import time
import argparse
import threading

from inc import EPILOG
from func import GetProgramPath

def ParseComandLine():
    parser = argparse.ArgumentParser(
        description="generate rsa public/private key pairs",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-n", "--nbits",
        dest="nbits",
        action="store",
        type=int,
        default=2048,
        help="the number of bits required to store n = p*q.",
        )
    parser.add_argument(
        "-d", "--ssh-folder",
        dest="sshfolder",
        action="store_true",
        help="store ssh-key pairs in ~/.ssh folder",
        )
    parser.add_argument(
        "-i", "--file-name",
        dest="filename",
        action="store",
        default="id_rsa",
        help="key pairs file name. default to id_rsa. and .pub is added to public key file."
        )
    parser.add_argument(
        "-f", "--force",
        dest="force",
        action="store_true",
        help="force to over write old key pair files.",
        )
    return parser, parser.parse_args()

def DotWriter():
    while 1:
        print(".", end="")
        os.sys.stdout.flush()
        time.sleep(1)

def RSAGen1(nbits):
    import rsa
    public_key, private_key = rsa.newkeys(nbits)
    return public_key.save_pkcs1(), private_key.save_pkcs1()

def Main():
    parser, opt = ParseComandLine()
    
    if opt.sshfolder:
        save_dir = os.path.join( os.path.expanduser("~"), ".ssh" )
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
    else:
        save_dir = os.getcwd()
    
    private_key_file_path = os.path.join(save_dir, opt.filename)
    public_key_file_path = os.path.join(save_dir, opt.filename+".pub")
    
    if not opt.force:
        flag = False
        if os.path.isfile(private_key_file_path):
            flag = True
            print("%s already exists."%(private_key_file_path))
        if os.path.isfile(public_key_file_path):
            flag = True
            print("%s already exists."%(public_key_file_path))
        if flag:
            r = input("Overwrite (y/n)?")
            if not r in ["y", "yes", "ok"]:
                os.sys.exit(0)
    
    dotwriter = threading.Thread(target=DotWriter)
    dotwriter.setDaemon(True)
    dotwriter.start()
    
    public_key, private_key = RSAGen1(opt.nbits)

    with open(public_key_file_path, "wb") as f:
        f.write(public_key)
    with open(private_key_file_path, "wb") as f:
        f.write(private_key)

    
if __name__ == '__main__':
    Main()
















