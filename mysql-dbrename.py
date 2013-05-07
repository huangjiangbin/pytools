import os
import argparse

from mysql.connector import Connect

from inc import EPILOG
from mysqlinc import AddMysqlParser

def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="Rename mysql database. Danger!!! read the sql statements before you --doit.",
        epilog=EPILOG,
        conflict_handler="resolve"
        )
    AddMysqlParser(parser)
    parser.add_argument(
        "--drop-old",
        dest="dropold",
        action="store_true",
        help="drop the old database",
        )
    parser.add_argument(
        "--doit",
        dest="doit",
        action="store_true",
        help="only show the sql statements will be executed",
        )
    parser.add_argument(
        "src",
        metavar="DB_OLD_NAME",
        nargs=1,
        help="the database's old name.",
        )
    parser.add_argument(
        "dst",
        metavar="DB_NEW_NAME",
        nargs=1,
        help="the database's new name.",
        )
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    opt.src = opt.src[0]
    opt.dst = opt.dst[0]
    
    if opt.src == opt.dst:
        print("new database name can not be the same with old.")
        os.sys.exit(1)
        
    conn = Connect(
            host=opt.mysql_host,
            port=opt.mysql_port,
            user=opt.mysql_user,
            password=opt.mysql_passwd,
            charset=opt.mysql_charset,
            use_unicode=True,
        )
    
    databases = []
    old_tables = []
    new_tables = []
    
    cursor = conn.cursor()
    cursor.execute("show databases")
    rows = cursor.fetchall()
    for row in rows:
        databases.append( row[0] )
    
    if not opt.src in databases:
        print("database %s not exists."%(opt.src))
        os.sys.exit(2)
    
    if not opt.dst in databases:
        sql = """
            SELECT
                SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
            FROM
                information_schema.SCHEMATA
            WHERE
                SCHEMA_NAME = %s
        """
        cursor.execute(sql, (opt.src,))
        rows = cursor.fetchall()
        row = rows[0]
        if row[0] == opt.src:
            DEFAULT_CHARACTER_SET_NAME = row[1]
            DEFAULT_COLLATION_NAME = row[2]
        else:
            print("load database charset setting failed!")
            os.sys.exit(3)
        
        sql = "CREATE DATABASE `%s` DEFAULT CHARACTER SET '%s' DEFAULT COLLATE '%s';"%(
            opt.dst, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME)
        print(sql)
        if opt.doit:
            cursor.execute(sql)
    
    cursor.execute("use %s"%(opt.src))
    cursor.execute("show tables")
    rows = cursor.fetchall()
    for row in rows:
        old_tables.append( "`%s`.`%s`"%(opt.src, row[0]) )
        new_tables.append( "`%s`.`%s`"%(opt.dst, row[0]) )
    for old_table, new_table in zip(old_tables, new_tables):
        sql = "ALTER TABLE %s RENAME TO %s;"%(old_table, new_table)
        print(sql)
        if opt.doit:
            cursor.execute(sql)
    
    if opt.dropold:
        sql = "DROP DATABASE `%s`;"%(opt.src)
        print(sql)
        if opt.doit:
            cursor.execute(sql)
            
if __name__ == '__main__':
    Main()