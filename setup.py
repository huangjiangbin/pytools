# encoding: utf-8
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
            
            # 字符串处理
            Executable("cat.py"),
            Executable("tail.py"),
            Executable("head.py"),
            Executable("eval.py"),
            Executable("crlf.py"),
            Executable("strip.py"),            
            Executable("lf.py"),
            Executable("lreplace.py"),
            Executable("lcount.py"),
            Executable("col.py"),
            Executable("uniq.py"),
            Executable("lsort.py"),
            Executable("sum.py"),
            
            # 字符串/数值/信号 生成器
            Executable("pwgen.py"),
            Executable("uuid4.py", targetName="uuid.exe"),
            Executable("urandom.py"),
            Executable("rand.py"),
            Executable("01switch.py"),
            Executable("ssh-keygen.py"),
            
            # 哈希算法
            Executable("b64.py", targetName="base64.exe"),
            Executable("hash.py"),
            Executable("hash.py", targetName="md5.exe"),
            Executable("hash.py", targetName="sha1.exe"),
            Executable("hash.py", targetName="sha224.exe"),
            Executable("hash.py", targetName="sha256.exe"),
            Executable("hash.py", targetName="sha384.exe"),
            Executable("hash.py", targetName="sha512.exe"),
            
            # 文件内容处理
            Executable("fstartswith.py"),
            Executable("fendswith.py"),            
            Executable("file.py"),
            
            # 系统时间相关程序
            Executable("nowtime.py"),
            Executable("isoweek.py"),
            Executable("uptime.py"),
            Executable("idletime.py"),
            Executable("cpuinfo.py"),
            
            # 输入控制/流程控制
            Executable("sleep.py"),
            Executable("pbreak.py"),
            Executable("getchar.py"),
            
            # 控制台窗口相关
            Executable("cmdsize.py"),
            Executable("cmdpid.py"),
            
            # 系统信息、环境变量
            Executable("pwd.py"),
            Executable("memfree.py"),
            Executable("dsnumber.py"),
            Executable("diskfree.py"),
            
            # 文件元信息
            Executable("fsize.py"),
            Executable("du.py"),
            Executable("fstat.py"),            
            Executable("fs.py"),
            
            # 文件查找
            Executable("which.py"),
            
            # 文件或文件夹操作
            Executable("touch.py"),
            
            # 网络客户端
            Executable("ping.py", targetName="yping.exe"),
            Executable("httpd.py"),
            Executable("ftpd.py"),
            Executable("whois.py"),
            Executable("urlget.py"),
            Executable("mailto.py"),
            
            # 图片相关操作
            Executable("iresize.py"),
            
            # 数据库相关操作
            Executable("mysql-dbrename.py"),
            
            # 其它特定用途工具
            Executable("css-grid-system.py"),
        ]
)