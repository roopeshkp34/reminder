from django.contrib import admin
from reminder.models import Person, LastDone
# Register your models here.

admin.site.register(Person)
admin.site.register(LastDone)