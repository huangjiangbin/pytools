import os
import socket
import argparse
from inc import EPILOG

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description = "Network client",
        epilog = EPILOG,
        conflict_handler="resolve"
        )
    parser.add_argument(
        "-r", "--crlf",
        dest="crlf",
        action="store_true",
        help="use CRLF as line break"
        )
    parser.add_argument(
        "-c", "--send-char",
        dest="sendchar",
        action="store_true",
        help="send char by char, or else it will do send after user press RETURN",
        )
    parser.add_argument(
        "-h", "--host",
        dest="host",
        action="store",
        required=True,
        help="target host",
        )
    parser.add_argument(
        "-p", "--port",
        dest="port",
        action="store",
        type=int,
        required=True,
        help="target port",
        )
    return parser, parser.parse_args()

class TelnetClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        
    def Connect(self):
        self.sock.connect( (self.host, self.port) )
    
    
def Main():
    parser, opt = ParseCommandLine()
    
if __name__ == '__main__':
    Main()






















