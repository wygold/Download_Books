# coding: utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.mime.application import MIMEApplication
import smtplib

account = "wygold@gmail.com"
password = ""

def send(to, title, content):
    smtp_port = 25
    server = smtplib.SMTP('smtp', smtp_port , timeout=120)
    server.ehlo()
    #server.starttls()
    server.set_debuglevel(1)
    #server.login(account, password)



    msg = MIMEText(content.encode('utf-8'))
    msg['Content-Type'] = 'text/plain; charset="utf-8"'
    msg['Subject'] = title
    msg['From'] = account
    msg['To'] = to
    server.sendmail(account, to, msg.as_string())
    server.close()

def send_with_attachment(to, title, content, files=None):
    smtp_port = 25
    msg = MIMEMultipart()
    msg['From'] = account
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = title

    msg.attach(MIMEText(content.encode('utf-8')))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=f.encode('utf-8')
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % f.encode('utf-8')
        msg.attach(part)

    smtp = smtplib.SMTP('smtp', smtp_port , timeout=120)
    smtp.set_debuglevel(1)
    smtp.sendmail(account, to, msg.as_string())
    smtp.close()

#send('wygold@gmail.com','test',u'content')
send_with_attachment(['wygold@gmail.com'],'test sbuject',u'book',[u'诡秘之主.txt'])