import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
from picamera import PiCamera
from time import sleep

camera = PiCamera()

def send_email(image_path):
    sender = 'niklashenningsen@gmx.net'
    password = input('Enter your email password: Ralf!2004.')
    recipient = 'madita.heinisch@gmx.de'
    subject = 'Raspberry Pi Image'
    body = 'Image captured by Raspberry Pi'
    server = 'mail.gmx.net'
    port = 587

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    with open(image_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    smtp.starttls()
    smtp.login(sender, password)
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.quit()

def capture_image():
    image_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'Images')
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    image_path = os.path.join(image_folder, 'image.jpg')
    
    camera.start_preview()
    sleep(5)
    camera.capture(image_path)
    camera.stop_preview()
    
    send_email(image_path)
    
    os.remove(image_path)

while True:
    key = input('Press 1 to capture an image: ')
    
    if key == '1':
        capture_image()
