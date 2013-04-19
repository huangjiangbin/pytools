import os



def GetProgramPath():
    if hasattr(os.sys, 'frozen'):
        return os.sys.executable
    else:
        return os.path.realpath(os.sys.argv[0])
