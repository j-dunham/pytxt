import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class EmailServer:
    def __init__(self, email, pwd):
        user, provider = email.split('@')
        self.server = smtplib.SMTP('smtp.{}'.format(provider), 587)
        self.usr = user
        self.pwd = pwd
        self.server.starttls()

    def send_txt(self, sender, recipient, message):
        self.server.login(self.usr, self.pwd)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg_txt = MIMEText(message)
        msg.attach(msg_txt)
        self.server.sendmail(sender, recipient, msg.as_string())
        self.server.quit()

    def send_pic(self, sender, recipient, message, pic_path):
        img_raw = open(pic_path, 'rb').read()
        img = MIMEImage(img_raw)

        self.server.login(self.usr, self.pwd)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg_txt = MIMEText(message)
        msg.attach(msg_txt)
        msg.attach(img)

        self.server.sendmail(sender, recipient, msg.as_string())
        self.server.quit()
