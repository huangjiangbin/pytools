import sys
from cx_Freeze import setup, Executable
from inc import *

includes = [
    "re",
]
include_files = [
    "etc/whois-servers.txt"
]
setup(
    name=PROGRAM_TITLE,
    version = VERSION,
    license = COPYRIGHT,
    description = "pytools",
    options = {
            "build_exe": {
                    "create_shared_zip": False,
                    "append_script_to_exe": True,
                    "include_in_shared_zip": False,
                    "includes": includes,
                    "include_files": include_files,
                },
        },
    executables = [
            Executable("pytools-version.py"),
            
            Executable("cat.py"),
            Executable("crlf.py"),
            Executable("strip.py"),            
            Executable("lf.py"),
            Executable("lreplace.py"),
            Executable("pwgen.py"),
            Executable("urandom.py"),
            Executable("b64.py", targetName="base64.exe"),
            
            Executable("hash.py"),
            Executable("hash.py", targetName="md5.exe"),
            Executable("hash.py", targetName="sha1.exe"),
            Executable("hash.py", targetName="sha224.exe"),
            Executable("hash.py", targetName="sha256.exe"),
            Executable("hash.py", targetName="sha384.exe"),
            Executable("hash.py", targetName="sha512.exe"),
            
            Executable("ssh-keygen.py"),
            
            Executable("pwd.py"),
            Executable("nowtime.py"),
            Executable("sleep.py"),
            
            Executable("getchar.py"),
            
            Executable("ftpd.py"),
            Executable("whois.py"),
            Executable("mailto.py"),
        ]
)