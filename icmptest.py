# encoding: utf-8
import os
import time
import socket
import struct
import ctypes
from ctypes.wintypes import *
import argparse
from inc import EPILOG

NULL = 0
UCHAR = ctypes.c_ubyte
PUCHAR = ctypes.POINTER(UCHAR)
ULONG = ctypes.c_ulong
USHORT = ctypes.c_ushort
PVOID = ctypes.c_void_p

class IPAddr(ctypes.Structure):
    _fields_ = [
            ("S_addr", ctypes.c_ulong)
        ]
    
    def __str__(self):
        return socket.inet_ntoa(struct.pack("L", self.S_addr))

def inet_addr(ip):
    return IPAddr( struct.unpack("L", socket.inet_aton(ip) )[0] )

class IP_OPTION_INFORMATION(ctypes.Structure):
    _fields_ = [
            ("Ttl", UCHAR),
            ("Tos", UCHAR),
            ("Flags", UCHAR),
            ("OptionsSize", UCHAR),
            ("OptionsData", PUCHAR),    
        ]

class ICMP_ECHO_REPLY(ctypes.Structure):
    _fields_ = [
            ("Address", IPAddr),
            ("Status", ULONG),
            ("RoundTripTime", ULONG),
            ("DataSize", USHORT),
            ("Reserved", USHORT),
            ("Data", PVOID),
            ("Options", IP_OPTION_INFORMATION),
        ]

GetLastError = ctypes.windll.kernel32.GetLastError

icmp = ctypes.windll.icmp

IcmpCreateFile = icmp.IcmpCreateFile
IcmpCreateFile.restype = HANDLE

IcmpCloseHandle = icmp.IcmpCloseHandle
IcmpCloseHandle.restype = BOOL

IcmpSendEcho = icmp.IcmpSendEcho
IcmpSendEcho.restype = DWORD

IP_STATUS_BASE              = 11000
  
IP_SUCCESS                  = 0
IP_BUF_TOO_SMALL            = (IP_STATUS_BASE + 1)
IP_DEST_NET_UNREACHABLE     = (IP_STATUS_BASE + 2)
IP_DEST_HOST_UNREACHABLE    = (IP_STATUS_BASE + 3)
IP_DEST_PROT_UNREACHABLE    = (IP_STATUS_BASE + 4)
IP_DEST_PORT_UNREACHABLE    = (IP_STATUS_BASE + 5)
IP_NO_RESOURCES             = (IP_STATUS_BASE + 6)
IP_BAD_OPTION               = (IP_STATUS_BASE + 7)
IP_HW_ERROR                 = (IP_STATUS_BASE + 8)
IP_PACKET_TOO_BIG           = (IP_STATUS_BASE + 9)
IP_REQ_TIMED_OUT            = (IP_STATUS_BASE + 10)
IP_BAD_REQ                  = (IP_STATUS_BASE + 11)
IP_BAD_ROUTE                = (IP_STATUS_BASE + 12)
IP_TTL_EXPIRED_TRANSIT      = (IP_STATUS_BASE + 13)
IP_TTL_EXPIRED_REASSEM      = (IP_STATUS_BASE + 14)
IP_PARAM_PROBLEM            = (IP_STATUS_BASE + 15)
IP_SOURCE_QUENCH            = (IP_STATUS_BASE + 16)
IP_OPTION_TOO_BIG           = (IP_STATUS_BASE + 17)
IP_BAD_DESTINATION          = (IP_STATUS_BASE + 18)

ICMP_ECHO_RESULT = {}
for k, v in dict(globals()).items():
    if k.startswith("IP_"):
        ICMP_ECHO_RESULT[v] = k

def Ping(host, seq=0, data_size=32, timeout=5000):
    try:
        ip = socket.gethostbyname(host)
    except:
        print("ping: unknown host %s"%(host))
        return 1
        
    send_data = b"github.com/huangjiangbin/pytools"
    if data_size-len(send_data):
        send_data += b"+"*(data_size-len(send_data))
    
    reply_buffer = ctypes.create_string_buffer( ctypes.sizeof(ICMP_ECHO_REPLY) + len(send_data) )
    ipaddr = inet_addr(ip)
    
    hIcmpFile = IcmpCreateFile()
    if hIcmpFile == -1:
        print("ping: system call IcmpCreateFile failed with error code %d"%(GetLastError()))
        return 2
    
    dwRetVal = IcmpSendEcho(
        hIcmpFile,
        ipaddr,
        send_data,
        len(send_data),
        0,
        reply_buffer,
        ctypes.sizeof(reply_buffer),
        timeout
        )
    reply_data = ICMP_ECHO_REPLY.from_buffer(reply_buffer)
    
    if dwRetVal < 1:
        print("ping: IcmpSendEcho not get reply info %d"%(GetLastError()))
        return 3
    
    error_code = reply_data.Status
    if error_code != IP_SUCCESS:
        error_msg = ICMP_ECHO_RESULT.get(error_code, "UNKNOWN")
        print("ping: IcmpSendEcho error %s [%d]"%(error_msg, error_code))
        return error_code
    
    if seq:
        str_icmp_seq = "seq=%d "%(seq)
    else:
        str_icmp_seq = ""
    
    info = "%d bytes from %s: %sttl=%d time=%.2f ms"%(
        reply_data.DataSize,
        ip,
        str_icmp_seq,
        reply_data.Options.Ttl,
        reply_data.RoundTripTime,
        )
    print(info)
    return 0

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="ping",
        epilog=EPILOG,
        )
    parser.add_argument(
        "-c", "--count",
        dest="count",
        action="store",
        default=4,
        type=int,
        help="how many times to do",
        )
    parser.add_argument(
        "-s", "--packetsize",
        dest="packetsize",
        action="store",
        default=32,
        type=int,
        help="data package size",
        )
    parser.add_argument(
        "host",
        metavar="DESTINATION",
        nargs=1,
        help="destination host or ip address",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    for seq in range(1, opt.count+1):
        t0 = time.time()
        Ping(opt.host[0], seq, opt.packetsize)
        t1 = time.time()
        td = 1000 - ( time.time()-t0 )
        if td > 0:
            time.sleep(td/1000.0)
            
if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        pass



