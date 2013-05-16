pytools
=======

PYTHON工具集（使用python3.3，面向windows开发）




特殊依赖
========
1. file工具
    1. magic.py是由python-magic-0.4.3修改而来的，放在pytools根目录下
        1. magic.py
    1. 需要将将libmagic相关的3个dll复制到pytools根目录下
        1. magic1.dll
        1. zlib1.dll
        1. regex2.dll
    1. 需要将相应的magic元数据库复制到pytools根目录下
        1. magic.mgc
