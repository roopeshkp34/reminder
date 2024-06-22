import smtplib
from email.message import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import secrets
import string

def generate_random_token(length=32):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token


def send_mail(to_email, name, token):
    from_email = settings.EMAIL
    from_password = settings.EMAIL_PASSWORD

    html_content = render_to_string('email/mail.html', {"name": name, "server": f"http://{settings.SERVER_DOMAIN}/not-available/{token}"})

    msg = EmailMessage()
    msg.set_content(f"Hi {name}, your the one to clean the kitchen waste today please do it today.")
    msg.add_alternative(html_content, subtype='html')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Daily Reminder"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

