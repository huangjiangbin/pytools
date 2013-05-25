pytools
=================================

PYTHON工具集（使用python3.3，面向windows开发）




特殊依赖
=================================
1. pywin32
    1. 打包程序需要pywin32的支持
    1. 利用ctypes直接调用DLL接口的程序需要pywin32
    1. 下载对应的pywin32安装包安装
1. cx_Freeze
    1. 用于发布Windows二进制包
    1. 下载对应的cx_Freeze安装包安装
1. libmagic
    1. 下载源代码(https://github.com/ahupp/python-magic)
        1. 执行 python setup.py install
    1. 需要将将libmagic相关的3个dll复制到pytools根目录下
        1. magic1.dll
        1. zlib1.dll
        1. regex2.dll
    1. 需要将相应的magic元数据库复制到pytools根目录下
        1. magic.mgc
1. PIL(pillow)
    1. 图片处理程序依赖于PIL模块
    1. 安装 pip install pillow
1. mysql-connector-python
    1. MYSQL相关工具依赖于mysql-connector-python模块
    1. mysql-connector-python是mysql官方提供的接口
    1. 安装 pip install mysql-connector-python
1. rsa
    1. ssh-keygen依赖于rsa模块
    1. 安装 pip insall rsa
1. wmi
    1. dsnumber获取磁盘序列号工具需要wmi模块
    1. cpuinfo也需要wmi模块
    1. 安装 pip install wmi
1. chardet2
    1. fencoding工具依赖于chardet模块
    1. 安装: pip install chardet2

版本冻结
=================================
2013-05-16
---------------------------------
1. 真郁闷，issue越做越多
1. 当issue数量超过100时，将进行版本冻结
1. 界时所有新功能或增强都归入下一个版本
1. 界时只接受BUG修改
1. 按现在的进度估计满100 issue能在本月完成
1. 6月份完成所有BUG的修正
1. 太难的issue也将转入新版本，甚至从项目中移除（目前已经开的issue中，网络客户端相关的功能，都比较有难度。比如ftp服务器，就完全可以独立为一个新项目上，telnet客户端也不简单吧。）

2013-05-24
---------------------------------
1. 今天issue总量超过了100
1. 所有新增功能保留到第二版本
1. 部分工作中急需的工具需要立即实现，仍然留在第一版本中

