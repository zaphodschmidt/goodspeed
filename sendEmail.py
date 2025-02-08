import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "szaphod@gmail.com"
receiver_email ="parkerjeanneallen@gmail.com"
# receiver_email ="zapschmidt@hotmail.com"
password = "wovw qiay gkbo ylfv"
subject = "Fuck you"
body = "This is from a python script that I made :) I love you"

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server details
    server.starttls()
    server.login(sender_email, password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()