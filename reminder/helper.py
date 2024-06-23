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

def generate_message_for_initial(to_email, name, token):
    try:
        html_content = render_to_string('email/mail.html', {"name": name, "server": f"http://{settings.SERVER_DOMAIN}/not-available/{token}"})

        msg = EmailMessage()
        msg.set_content(f"Hi {name}, your the one to clean the kitchen waste today please do it today.")
        msg.add_alternative(html_content, subtype='html')
        msg['From'] = settings.EMAIL
        msg['To'] = to_email
        msg['Subject'] = "Daily Reminder"

        send_mail(msg)
    except: raise Exception

def generate_message_for_re_assign(to_email, name, token, pervious_person):
    try:
        html_content = render_to_string('email/reassign-mail.html', {"name": name, "server": f"http://{settings.SERVER_DOMAIN}/not-available/{token}", "pervious_person": pervious_person})

        msg = EmailMessage()
        msg.set_content(f"Hi {name}, your the one to clean the kitchen waste today please do it today.")
        msg.add_alternative(html_content, subtype='html')
        msg['From'] = settings.EMAIL
        msg['To'] = to_email
        msg['Subject'] = "Daily Reminder"

        send_mail(msg)
    except: raise Exception


def send_mail(message: EmailMessage):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL, settings.EMAIL_PASSWORD)
        server.send_message(message)
        server.quit()
        print(f"""Email sent to {message["To"]}""")
    except Exception as e:
        print(f"""Failed to send email to {message["To"]}. Error: {e}""")
        raise Exception

