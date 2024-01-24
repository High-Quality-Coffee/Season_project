import os
import season
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# config = wiz.model("portal/season/config")
struct = wiz.model("portal/gram/struct")
# config = wiz.config("gram")
config = struct.config
SMTP_SENDER = config.get("smtp_sender")
SMTP_HOST = config.get("smtp_host")
SMTP_PORT = config.get("smtp_port")
SMTP_PASSWORD = config.get("smtp_password")
# SMTP_SENDER = config.smtp_sender
# SMTP_HOST = config.smtp_host
# SMTP_PORT = config.smtp_port
# SMTP_PASSWORD = config.smtp_password
fs = wiz.workspace("service").fs(os.path.join("config", "smtp"))

class Model:
    def __init__(self):
        pass
    
    def randomcode(self, length=6):
        string_pool = string.digits
        result = ""
        for i in range(length):
            result += random.choice(string_pool)
        return result

    def send(self, to, title="TITLE", body="", **kwargs):
        sender = SMTP_SENDER
        html = body
        for key in kwargs:
            try:
                html = html.replace("{" + key + "}", str(kwargs[key]))
            except:
                pass
            try:
                title = title.replace("{" + key + "}", str(kwargs[key]))
            except:
                pass

        msg = MIMEText(html, 'html', _charset='utf8')
        msg['Subject'] = title
        msg['From'] = SMTP_SENDER
        msg['To'] = to

        mailserver = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(SMTP_SENDER, SMTP_PASSWORD)
        mailserver.sendmail(SMTP_SENDER, to, msg.as_string())
        mailserver.quit()
    
    @classmethod
    def use(cls):
        return cls()