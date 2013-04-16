from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS


class VFS(AbstractedFS):
    def __init__(self, root, cmd_channel):
        super(VFS, self).__init__(root, cmd_channel)
        print("====file system init====")
        print(root)
        print(cmd_channel)

    def ftp2fs(self, ftppath):
        r = super(VFS, self).ftp2fs(ftppath)
        print("ftp2fs: %s %s"%(ftppath, r))
        return r.replace("e:", "f:")
    
    def validpath(self, path):
        return True
    
authorizer = DummyAuthorizer()
authorizer.add_user("admin", "123456", "e:/", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer
handler.abstracted_fs = VFS

server = FTPServer( ("127.0.0.1", 21), handler )
server.serve_forever()