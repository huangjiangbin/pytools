import os
import time
import datetime
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
        help="Config file.",
        )
    parser.add_argument(
        "-s", "--section",
        dest="section",
        action="store",
        required=True,
        help="The main section name in the config file.",
        )
    parser.add_argument(
        "-l", "--log",
        metavar="FILE",
        dest="log",
        action="store",
        help="Log the xml content to the FILE.",
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
    for c in range(1,5):
        try:
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
        except:
            pass
        time.sleep(c)
    os.sys.exit(1)
    
def GetRows(config, opt, sql):
    for c in range(1,5):
        try:
            conn = GetConn(config, opt)
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows, cursor.column_names
        except:
            pass
        time.sleep(c)
    os.sys.exit(1)
    

def XmlPipe2Begin(global_config, opt):
    section_config = global_config[opt.section]
    str_fields = ""
    str_attrs = ""
    
    fields = section_config["fields"].splitlines()
    for field in fields:
        field = field.strip()
        if field:
            str_fields += """\t\t<sphinx:field name="%s" />\n"""%(field)
    
    types = ["int", "uint", "timestamp", "bool", "float", "string", "multi"]
    for ctype in types:
        if ctype == "uint" or ctype == "int":
            ctype_name = "int"
            ext = """bits="32" """
        else:
            ctype_name = ctype
            ext = ""
        attrs = section_config.get(ctype+"_attrs", "").splitlines()
        for attr in attrs:
            attr = attr.strip()
            if attr:
                str_attrs += """\t\t<sphinx:attr name="%s" type="%s" %s/>\n"""%(attr, ctype_name, ext)
    
    MyPrint("""<?xml version="1.0" encoding="utf-8"?>""")
    MyPrint("""<sphinx:docset>""")
    MyPrint("""\t<sphinx:schema>\n%s%s\t</sphinx:schema>"""%(str_fields, str_attrs))
    
def XmlPipe2End():
    MyPrint("""</sphinx:docset>""")

def RowsHandler(rs, config, opt):
    rows = rs[0]
    fieldnames = rs[1]
    fcount = len(fieldnames)
    mvas = LoadMVAs(config, opt)
    
    for row in rows:
        id = row[0]
        MyPrint("""\t<sphinx:document id="%d">"""%(id))
        for col in range(1, fcount):
            k = fieldnames[col]
            v = row[col]
            if v is None:
                v = ""
            if isinstance(v, datetime.datetime):
                v = int(time.mktime( v.timetuple() ))
            v = str(v)
            if ("<" in v) or (">" in v) or ("&" in v):
                v = "<![CDATA[[" + v + "]]>"
            if v:
                MyPrint("""\t\t<%s>%s</%s>"""%(k, v, k))
            else:
                MyPrint("""\t\t<%s />"""%(k))
        for field_name in mvas:
            if id in mvas[field_name]:
                MyPrint("""\t\t<%s>%s</%s>"""%(field_name, mvas[field_name][id], field_name))
        MyPrint("""\t</sphinx:document>""")

global_mvas = None
def LoadMVAs(global_config, opt):
    global global_mvas
    
    if not global_mvas is None:
        return global_mvas
    
    global_mvas = {}
    global_config = LoadConfig(opt.config)
    section_config = global_config[opt.section]
    fields = section_config.get("multi_attrs", "").splitlines()
    for field in fields:
        field = field.strip()
        if field:
            if not field in global_mvas:
                global_mvas[field] = {}
            field_mvas = global_mvas[field]
            sql = section_config.get(field+"_query", "").strip()
            if sql:
                rows, _ = GetRows(global_config, opt, sql)
                aids = list(set([row[0] for row in rows]))
                for aid in aids:
                    field_mvas[aid] = []
                for row in rows:
                    field_mvas[row[0]].append(str(row[1]))
            for k in field_mvas:
                field_mvas[k] = ",".join(list(set(field_mvas[k])))
    return global_mvas
    
global_log_file = ""
global_log_file_object = None

def Log(line):
    global global_log_file_object
    
    if not global_log_file:
        return
    
    if global_log_file_object is None:
        global_log_file_object = open(global_log_file, "wb")
    
    global_log_file_object.write(line)
    
def MyPrint(line):
    line += "\n"
    line = line.encode("utf-8")
    
    Log(line)
    os.sys.stdout.buffer.write(line)

def Main():
    global global_log_file_object
    global global_log_file
    
    parser, opt = ParseCommandLine()
    global_config = LoadConfig(opt.config)
    section_config = global_config[opt.section]
    
    if opt.log:
        global_log_file = opt.log
    
    MVAs = LoadMVAs(global_config, opt)

    XmlPipe2Begin(global_config, opt)
    
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
            
            start_id += step + 1
            if start_id > max_id:
                break
    else:
        sql = sql_query
        rs = GetRows(global_config, opt, sql)
        RowsHandler(rs, global_config, opt)
    
    XmlPipe2End()
    
    if global_log_file_object:
        global_log_file_object.flush()
        global_log_file_object.close()

if __name__ == '__main__':
    try:
        Main()
    finally:
        if global_log_file_object:
            global_log_file_object.close()
