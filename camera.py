import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
import time
from picamera import PiCamera

camera = PiCamera()

def send_mail(send_from, send_to, subject, message, files=[],
              server="mail.gmx.net", port=587, username='', password='',
              use_tls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(os.path.basename(path)))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

# E-Mail-Konfiguration
email_username = "niklashenningsen@gmx.net"
email_password = "Ralf!2004."
email_sender = email_username
email_recipient = ["niklas_henningsen@icloud.com"]  # Empfänger-E-Mail-Adresse

while True:
    key = input("Drücke 1, um ein Foto aufzunehmen: ")
    if key == "1":
        camera.capture('/home/pi/Desktop/image.jpg')
        send_mail(email_sender, email_recipient, "Foto von Raspberry Pi",
                  "Hier ist das Foto von deinem Raspberry Pi!",
                  ["/home/pi/Desktop/image.jpg"],
                  username=email_username, password=email_password)
