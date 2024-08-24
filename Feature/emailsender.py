import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_whom, subject, content):
    sender_mail = "shogangaikwad786@gmail.com"
    sender_pass = "gbmuyrepfufwiyrk"  # Use your App Password here
    receiver_mail = to_whom

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_mail
        msg['To'] = receiver_mail
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_mail, sender_pass)
            server.sendmail(sender_mail, receiver_mail, msg.as_string())
            print("Email sent successfully")

    except smtplib.SMTPAuthenticationError as auth_error:
        print(f"Authentication failed. Check your username and password. Error: {auth_error}")
    except smtplib.SMTPException as smtp_error:
        print(f"SMTP error: {smtp_error}")
    except Exception as e:      
        print(f'Error: {e}')
