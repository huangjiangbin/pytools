import sys
from cx_Freeze import setup, Executable

includes = [
    "re",
]
include_files = [
]
setup(
    name="pytools",
    version = "0.1",
    description = "pytools",
    options = {"build_exe": {"includes": includes, "include_files": include_files}},
    executables = [
            Executable("cat.py"),
            Executable("pwd.py"),
            Executable("pwgen.py"),
            Executable("urandom.py"),
            Executable("ftpd.py"),
        ]
)