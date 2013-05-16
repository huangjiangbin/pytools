import sys
from cx_Freeze import setup, Executable
from inc import *

includes = [
    "re",
]
include_files = [
    "etc/whois-servers.txt",
    "magic1.dll",
    "regex2.dll",
    "zlib1.dll",
    "magic.mgc",
]
setup(
    name=PROGRAM_TITLE,
    version = VERSION,
    license = COPYRIGHT,
    description = "pytools",
    options = {
            "build_exe": {
                    #"create_shared_zip": False,
                    #"append_script_to_exe": True,
                    #"include_in_shared_zip": False,
                    "includes": includes,
                    "include_files": include_files,
                },
        },
    executables = [
            Executable("pytools-version.py"),
            
            Executable("cat.py"),
            Executable("tail.py"),
            Executable("head.py"),
            Executable("file.py"),
            
            Executable("crlf.py"),
            Executable("strip.py"),            
            Executable("lf.py"),
            Executable("lreplace.py"),
            Executable("lcount.py"),
            Executable("col.py"),
            Executable("uniq.py"),
            Executable("lsort.py"),
            Executable("sum.py"),
            
            Executable("pwgen.py"),
            Executable("uuid4.py", targetName="uuid.exe"),
            Executable("urandom.py"),
            Executable("rand.py"),
            Executable("switch01.py"),
            
            Executable("fstartswith.py"),
            Executable("fendswith.py"),
            
            Executable("b64.py", targetName="base64.exe"),
            Executable("hash.py"),
            Executable("hash.py", targetName="md5.exe"),
            Executable("hash.py", targetName="sha1.exe"),
            Executable("hash.py", targetName="sha224.exe"),
            Executable("hash.py", targetName="sha256.exe"),
            Executable("hash.py", targetName="sha384.exe"),
            Executable("hash.py", targetName="sha512.exe"),
            
            Executable("ssh-keygen.py"),
            
            Executable("nowtime.py"),
            Executable("isoweek.py"),
            Executable("uptime.py"),
            Executable("idletime.py"),
            Executable("sleep.py"),
            
            Executable("cmdsize.py"),
            Executable("pwd.py"),
            Executable("fs.py"),
            Executable("which.py"),
            Executable("du.py"),
            Executable("fstat.py"),
            Executable("touch.py"),
            Executable("cd.py", targetName="goto.exe"),
            
            Executable("dsnumber.py"),
            
            Executable("ppid.py"),
            Executable("memfree.py"),
            Executable("diskfree.py"),
            
            Executable("getchar.py"),
            
            Executable("ping.py", targetName="yping.exe"),
            Executable("httpd.py"),
            Executable("ftpd.py"),
            Executable("whois.py"),
            Executable("wget.py"),
            Executable("mailto.py"),
            
            Executable("iresize.py"),
            
            Executable("mysql-dbrename.py"),
            
            Executable("css-grid-system.py"),
        ]
)