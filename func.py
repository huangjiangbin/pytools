import os



def GetProgramPath():
    if hasattr(os.sys, 'frozen'):
        return os.sys.executable
    else:
        return os.path.realpath(os.sys.argv[0])

def StripCRLF(s):
    if not s:
        return s
    
    crlf = "\r\n"
    cr = "\r"
    lf = "\n"
    if isinstance(s, (bytes, bytearray)):
        crlf = b"\r\n"
        cr = b"\r"
        lf = b"\n"
        
    if s[-2:] == crlf:
        return s[:-2]
    if s[-1:] == lf or s[-1:] == cr:
        return s[:-1]
    return s

def SmartUnicode(s):
    if isinstance(s, str):
        return s
    if isinstance(s, (bytes, bytearray)):
        encodings = ["utf-8", "gb18030", "iso-8859-1", "windows-1252", "windows-1253"]
        for encoding in encodings:
            try:
                return s.decode(encoding)
            except UnicodeDecodeError:
                pass
        return ""
    return str(s)

def StdoutWrite(line):
    try:
        os.sys.stdout.buffer.write(line)
        os.sys.stdout.buffer.flush()
        flag = True
    except:
        flag = False
    
    if not flag:
        os.sys.exit(1)

def StdinSize():
    try:
        size = os.sys.stdin.seek(0, 2)
        os.sys.stdin.seek(0, 0)
    except:
        size = 0
    return size

