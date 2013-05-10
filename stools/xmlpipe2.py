import os
import configparser
import argparse

from mysql.connector import Connect as MysqlConnect


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="sphinx searchd database source as xmlpip2 format",
        )
    parser.add_argument(
        "-c", "--config",
        dest="config",
        action="store",
        required=True,
        help="config file.",
        )
    parser.add_argument(
        "-s", "--section",
        dest="section",
        action="store",
        required=True,
        help="second name in config file.",
        )
    parser.add_argument(
        "-a", "--action",
        choices=["all", "delta"],
        dest="action",
        action="store",
        help="generator action.",
        )
    return parser, parser.parse_args()

def LoadConfig(f):
    cobj = configparser.ConfigParser()
    cobj.read(f)
    return cobj

def GetConn(config, opt):
    scfg = config[opt.section]
    dcfg = config[scfg["database"]]
    return MysqlConnect(
            host=dcfg["host"],
            port=int(dcfg.get("port", 3306)),
            user=dcfg["username"],
            password=dcfg["password"],
            database=dcfg["database"],
            autocommit=dcfg.get("autocommit", True),
            charset=dcfg.get("charset", "utf8"),
        )

def GetMinMaxID(config, opt):
    cfg = config[opt.section]
    sql = "select min(%s) as min_id, max(%s) as max_id from %s;"%(
            cfg.get("id_field", "id"),
            cfg.get("id_field", "id"),
            cfg["table"],
        )
    
    conn = GetConn(config, opt)
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()[0]

def GetRows(config, opt, sql):
    conn = GetConn(config, opt)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    fieldnames = []
    for f in cursor.description:
        fieldnames.append( f[0] )
    return rows, fieldnames

def XmlPip2Begin(global_config, opt):
    section_config = global_config[opt.section]
    str_fields = ""
    str_attrs = ""
    
    fields = section_config["fields"].splitlines()
    for field in fields:
        field = field.strip()
        if field:
            str_fields += """\t\t<sphinx:field name="%s" />\n"""%(field)
    
    types = ["uint", "bigint", "float", "timestamp", "string", "multi"]
    for ctype in types:
        attrs = section_config.get(ctype+"_attrs", "").splitlines()
        for attr in attrs:
            attr = attr.strip()
            if attr:
                str_attrs += """\t\t<sphinx:attr type="%s" name="%s" />\n"""%(ctype, attr)

    print("""<?xml version="1.0" encoding="utf-8"?>""")
    print("""<sphinx:docset>""")
    print("""\t<sphinx:schema>\n%s%s\t</sphinx:schema>"""%(str_fields, str_attrs))

def XmlPip2End():
    print("""</sphinx:docset>""")

def RowsHandler(rs, config, opt):
    rows = rs[0]
    fieldnames = rs[1]
    fcount = len(fieldnames)
    
    for row in rows:
        id = row[0]
        print("""\t<sphinx:document id="%d">"""%(id))
        for col in range(1, fcount):
            k = fieldnames[col]
            v = str(row[col])
            if ("<" in v) or (">" in v):
                v = "<![CDATA[[" + v + "]]>"
            print("""\t\t<%s>%s</%s>"""%(k, v, k))
        # todo: print multi field values
        print("""\t</sphinx:document>""")

def Main():
    parser, opt = ParseCommandLine()
    global_config = LoadConfig(opt.config)
    section_config = global_config[opt.section]
    
    XmlPip2Begin(global_config, opt)
    
    sql_query = section_config["sql_query"]
    if ("$start" in sql_query) or ("$end" in sql_query):
        min_id, max_id = GetMinMaxID(global_config, opt)
        step = int(section_config.get("step", 4096))
        start_id = min_id
        while 1:
            end_id = start_id + step
            sql = sql_query
            sql = sql.replace("$start", str(start_id)).replace("$end", str(end_id))
            
            rs = GetRows(global_config, opt, sql)
            RowsHandler(rs, global_config, opt)
            
            start_id += step
            if start_id > max_id:
                break
    else:
        sql = sql_query
        rs = GetRows(global_config, opt, sql)
        RowsHandler(rs, global_config, opt)
    
    XmlPip2End()
    
if __name__ == '__main__':
    Main()
