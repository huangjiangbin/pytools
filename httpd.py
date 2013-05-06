import os
from http.server import HTTPServer, CGIHTTPRequestHandler, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="simple static http server",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-d", "--directory",
        dest="directory",
        action="store",
        default=".",
        help="Document root directory. Default to use current folder.",
        )
    parser.add_argument(
        "--cgi",
        action="store_true",
        help="Run as CGI Server",
        )
    parser.add_argument(
        "-p", "--port",
        dest="port",
        action="store",
        type=int,
        default=80,
        help="Specify alternate port [default: 80]",
        )
    return parser, parser.parse_args()

class MultiThreadServerClass(ThreadingMixIn, HTTPServer):
    pass

def RunTestServer(HandlerClass=BaseHTTPRequestHandler, ServerClass=HTTPServer, protocol="HTTP/1.0", port=80):
    
    server_address = ('', port)

    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    
    while True:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            httpd.server_close()
            os.sys.exit(0)
        
def Main():
    parser, opt = ParseCommandLine()
    
    if opt.directory != ".":
        folder = os.path.realpath(opt.directory)
        os.chdir(folder)
    
    if opt.cgi:
        RunTestServer(ServerClass=MultiThreadServerClass, HandlerClass=CGIHTTPRequestHandler, port=opt.port)
    else:
        RunTestServer(ServerClass=MultiThreadServerClass, HandlerClass=SimpleHTTPRequestHandler, port=opt.port)
        
if __name__ == '__main__':
    Main()









