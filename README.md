pytools
=======

PYTHON工具集（使用python3.3，面向windows开发）




特殊依赖
========
1. file工具
    1. magic.py是由python-magic-0.4.3修改而来的，需要独立安装扩展
        1. python-magic (https://github.com/ahupp/python-magic)
    1. 需要将将libmagic相关的3个dll复制到pytools根目录下
        1. magic1.dll
        1. zlib1.dll
        1. regex2.dll
    1. 需要将相应的magic元数据库复制到pytools根目录下
        1. magic.mgc


版本冻结
========
1. 真郁闷，issue越做越多
1. 当issue数量超过100时，将进行版本冻结
1. 界时所有新功能或增强都归入下一个版本
1. 界时只接受BUG修改
1. 按现在的进度估计满100 issue能在本月完成
1. 6月份完成所有BUG的修正
1. 太难的issue也将转入新版本，甚至从项目中移除（目前已经开的issue中，网络客户端相关的功能，都比较有难度。比如ftp服务器，就完全可以独立为一个新项目上，telnet客户端也不简单吧。）
1. 2013-05-16
