import os
import re
import socket
from urllib.request import urlopen
import argparse
from inc import EPILOG

def force_unicode(bstr):
    try:
        return bstr.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return bstr.decode("gb18030")
        except UnicodeDecodeError:
            try:
                return bstr.decode("iso-8859-15")
            except UnicodeDecodeError:
                return ""
            
def LoadWhoisServers(whois_server_list_file, whois_server_list_source_url, force_reload=False):
    servers = {}
    rows = []
    try:
        list_file = os.path.join( os.path.dirname(os.sys.executable), whois_server_list_file )
    except:
        list_file = os.path.realpath(os.path.join( os.path.realpath(os.path.dirname(os.sys.argv[0])), whois_server_list_file ))
        
    if list_file and (not force_reload):
        try:
            with open(list_file) as f:
                rows = f.readlines()
        except:
            pass
    if not rows:
        text = urlopen(whois_server_list_source_url).read()
        text = force_unicode(text)
        if not text:
            print("load whois servers from %s failed."%(whois_server_list_source_url))
            os.sys.exit(1)
            
        if list_file:
            try:
                folder = os.path.dirname(list_file)
                if not os.path.isdir(folder):
                    os.makedirs(folder)
                with open(list_file, "wb") as f:
                    f.write(text.encode("utf-8"))
            except:
                pass
        rows = text.splitlines()
        
    if rows:
        for row in rows:
            row = row.strip()
            if not row:
                continue
            if row.startswith(";") or row.startswith("#"):
                continue
            rs = row.split(" ")
            if len(rs) == 2:
                top = rs[0]
                server = rs[1]
                servers[top] = server
    
    return servers


def ParserCommandLine():
    parser = argparse.ArgumentParser(
        description = "get domain register infos",
        epilog = EPILOG,
        )
    parser.add_argument(
        "-c", "--cache-file",
        dest="file",
        action="store",
        default="etc/whois-servers.txt",
        help="whois servers cache file. default etc/whois-servers.txt",
        )
    parser.add_argument(
        "-s", "--source-url",
        dest="url",
        action="store",
        default="http://www.nirsoft.net/whois-servers.txt",
        help="whois servers online source url. default http://www.nirsoft.net/whois-servers.txt",
        )
    parser.add_argument(
        "-f", "--force-reload",
        dest="force",
        action="store_true",
        help="force to reload whois servers from source url. default is False, using servers in cache file.",
        )
    parser.add_argument(
        "domain",
        nargs=1,
        )
    return parser, parser.parse_args()

def Query(server, domain):
    s = socket.socket()
    s.connect( (server, 43) )
    s.sendall( (domain+"\r\n").encode("utf-8") )
    info = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        info += data
    
    return force_unicode( info )

def Main():
    parser, opt = ParserCommandLine()
    whois_servers = LoadWhoisServers(opt.file, opt.url, opt.force)
    domain = opt.domain[0].strip()
    top = domain
    while True:
        if top in whois_servers:
            break
        top = ".".join(top.split(".")[1:])
        if not top:
            break
    if (not top) or (not top in whois_servers):
        print( "do not kown this kind domain" )
        os.sys.exit(2)
        
    server = whois_servers[top]
    info = Query(server, domain)
    if "=xxx" in info:
        info = Query(server, "="+domain)
    print(info)
    
    bad_keywords = ["error:", "=xxx", "no data", "not found", "no match", "not match", "invalid domain", "no records"]
    real_whois_servers = set()
    rs = re.findall("Whois Server:(.*)\n", info)
    for r in rs:
        r = r.strip()
        real_whois_servers.add(r)
    real_whois_servers = list(real_whois_servers)
    if len(real_whois_servers) > 0:
        for real_whois_server in real_whois_servers:
            real_whois_server = real_whois_server.strip()
            if server == real_whois_server:
                continue
            info = Query(real_whois_server, domain)
            info2 = info.lower()
            bad_flag = False
            for keyword in bad_keywords:
                if keyword in info2:
                    bad_flag = True
                    break
            if not bad_flag:
                print(info)
            else:
                pass
    
if __name__ == '__main__':
    Main()
