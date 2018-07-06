import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

mms_carriers = {
    "straight_talk": "mypixmessages.com",
    "at&t": "mms.att.net",
    "verizon": "vzwpix.com",
}
sms_carriers = {
    "straight_talk": "vtext.com",
    "at&t": "txt.att.net",
    "verizon": "vtext.com",
}


class Recipient:
    def __init__(self, name: str, phone_number: str, carrier_name: str) -> None:
        self.name = name
        self.phone_number = phone_number
        self.carrier_name = carrier_name
        self.sms_address = f"{phone_number}@{sms_carriers.get(carrier_name)}"
        self.mms_address = f"{phone_number}@{mms_carriers.get(carrier_name)}"


class Sender:
    def __init__(self, email: str, pwd: str) -> None:
        self.user = email.split("@")[0]
        self.provider = email.split("@")[1]
        self.pwd = pwd
        self.server: smtplib.SMTP = None

    def start_server(self) -> None:
        self.server = smtplib.SMTP("smtp.{}".format(self.provider), 587)
        self.server.starttls()
        self.server.login(self.user, self.pwd)

    def stop_server(self) -> None:
        if self.server is not None:
            self.server.quit()
            self.server = None

    def send_txt(
        self,
        recipient: Recipient,
        message: str,
        image_path: str = None,
        use_mms: bool = True,
    ) -> None:
        self.start_server()
        if use_mms:
            address = recipient.mms_address
        else:
            address = recipient.sms_address
        msg = self.construct_message(address, message=message, image_path=image_path)
        self.server.sendmail("", address, msg.as_string())
        self.server.quit()

    @staticmethod
    def construct_message(
        address: str, message: str, image_path: str = None
    ) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = ""
        msg["To"] = address
        msg_txt = MIMEText(message)
        msg.attach(msg_txt)
        if image_path is not None:
            img_raw = open(image_path, "rb").read()
            img = MIMEImage(img_raw)
            msg.attach(img)
        return msg


class Receiver:
    def __init__(self, user: str, pwd: str, provider: str):
        self.imap_server: imaplib.IMAP4_SSL = None
        self.user = user
        self.pwd = pwd
        self.provider = provider

    def start(self):
        self.imap_server = imaplib.IMAP4_SSL(f"imap.{self.provider}")
        self.imap_server.login(self.user, self.pwd)

    def stop(self):
        if self.imap_server is not None:
            self.imap_server.logout()
            self.imap_server = None


class Conversation:
    def __init__(self, sender: Sender, recipient: Recipient):
        self.sender: Sender = sender
        self.recipient: Recipient = recipient
        self.receiver: Receiver = None

    def say(self, message: str, use_mss=True):
        self.sender.send_txt(recipient=self.recipient, message=message, use_mms=use_mss)

    def start_receiver(self):
        self.receiver = Receiver(
            self.sender.user, self.sender.pwd, self.sender.provider
        )
        self.receiver.start()

    def stop_receiver(self):
        if self.receiver is not None:
            self.receiver.stop()
        self.receiver = None

    def check(self):
        self.start_receiver()
        self.receiver.imap_server.select("INBOX")
        result = self.receiver.imap_server.search(
            None, f'(FROM "{self.recipient.sms_address}" UNSEEN)'
        )
        self.receiver.stop()
        return result
