



def GetConn(opt):
    return Connect(
        host=opt.mysql_host,
        port=opt.mysql_port,
        user=opt.mysql_
    )

def AddMysqlParser(parser):
    parser.add_argument_group("mysql")
    parser.add_argument(
        "-h", "--host",
        metavar="HOST",
        dest="mysql_host",
        action="store",
        default="127.0.0.1",
        help="mysql host",
        )
    parser.add_argument(
        "-P", "--port",
        metavar="PORT",
        dest="mysql_port",
        action="store",
        type=int,
        default=3306,
        help="mysql port",
        )
    parser.add_argument(
        "-u", "--user",
        metavar="USER",
        dest="mysql_user",
        action="store",
        default="root",
        help="mysql user",
        )
    parser.add_argument(
        "-p", "--passwd",
        metavar="PASSWD",
        dest="mysql_passwd",
        action="store",
        default="",
        help="mysql passwd",
        )
    parser.add_argument(
        "-c", "--charset",
        metavar="CHARSET",
        dest="mysql_charset",
        action="store",
        default="utf8",
        help="mysql connection charset",
        )
    