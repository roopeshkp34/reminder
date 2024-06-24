import os
env = os.environ
env.setdefault("DJANGO_SETTINGS_MODULE", "mail_reminder.settings")
import django
django.setup()

from django.contrib.auth.models import User

if (User.objects.filter(username= env["ADMIN_USERNAME"]).count()) == 0:
    User.objects.create_superuser(username= env["ADMIN_USERNAME"], password=env["ADMIN_PASSWORD"])

print(f"User Exist")