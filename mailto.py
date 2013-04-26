# encoding: utf-8
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import argparse
from inc import EPILOG


def ParseCommandLine():
    parser = argparse.ArgumentParser(
        description="send email",
        epilog=EPILOG,
        conflict_handler="resolve",
        )
    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="debug mode",
        )
    parser.add_argument(
        "-h", "--host",
        dest="smtp_host",
        action="store",
        default="localhost",
        help="smtp server hostname or ip address",
        )
    parser.add_argument(
        "-p", "--port",
        dest="smtp_port",
        action="store",
        type=int,
        default=25,
        help="smtp server port",
        )
    parser.add_argument(
        "-u", "--username",
        dest="smtp_username",
        action="store",
        help="smtp user account",
        )
    parser.add_argument(
        "-P", "--password",
        dest="smtp_password",
        action="store",
        help="smtp user password",
        )
    parser.add_argument(
        "-s", "--sender",
        dest="sender",
        action="store",
        required=True,
        help="sender name and email address"
        )
    parser.add_argument(
        "-r", "--receivers",
        dest="receivers",
        nargs="+",
        required=True,
        help="receiver names and email addresses"
        )
    parser.add_argument(
        "-t", "--subject",
        dest="subject",
        action="store",
        help="email subject",
        )
    parser.add_argument(
        "-a", "--attachments",
        dest="attachments",
        action="store",
        nargs="*",
        help="attachment files",
        )
    parser.add_argument(
        "-e", "--encoding",
        dest="encoding",
        action="store",
        default="utf-8",
        help="content encoding",
        )
    parser.add_argument(
        "-m", "--mimetype",
        dest="mimetype",
        action="store",
        default="html",
        help="content encoding",
        )    
    parser.add_argument(
        "contentfile",
        metavar="CONTENT",
        nargs="?",
        default="-",
        help="email content",
        )   
    return parser, parser.parse_args()

def Main():
    parser, opt = ParseCommandLine()
    
    # 处理 发件人
    sender = opt.sender
    if ("<" in sender) and (">" in sender):
        sender = re.findall( "\<(.*)\>", sender )[0]
    
    # 处理 收件人
    receivers = []
    for receiver in opt.receivers:
        if ("<" in receiver) and (">" in receiver):
            receiver = re.findall( "\<(.*)\>", receiver )[0]
        receivers.append(receiver)
    
    # 处理正文基本信息
    msg = MIMEMultipart("alternative")
    msg["From"] = opt.sender
    msg["To"] = ", ".join( opt.receivers )
    if opt.subject:
        msg["Subject"] = opt.subject
    
    # 处理正文内容
    if opt.contentfile == "-":
        content = os.sys.stdin.buffer.read().decode(opt.encoding)
    else:
        with open(opt.contentfile, r, encoding=opt.encoding) as f:
            content = f.read()
    msg.attach( MIMEText(content, opt.mimetype) )
    
    # 处理附件
    for attachment in opt.attachments:
        with open(attachment, "rb") as f:
            filename = os.path.split(attachment)[1]
            ext = os.path.splitext(filename)[1].lower()
            if ext in [".gif", ".jpg", ".jpeg", ".png", ".bmp"]:
                p = MIMEImage( f.read() )
            else:
                p = MIMEApplication( f.read() )
            p.add_header( "Content-Disposition", 'attachment; filename="%s"'%(filename) )
            p.add_header( "Content-ID""", filename )
            msg.attach( p )
    
    # 发送邮件
    proxy = smtplib.SMTP(opt.smtp_host, opt.smtp_port)
    
    if opt.verbose:
        proxy.set_debuglevel(1)
        
    if opt.smtp_password:
        username = opt.smtp_username
        if not username:
            username = sender
        proxy.login(username, opt.smtp_password)
        
    proxy.sendmail(sender, receivers, msg.as_string())
    
if __name__ == '__main__':
    Main()
    

