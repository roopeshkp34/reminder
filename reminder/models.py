from django.db import models

# Create your models here.

"""anjuraj0511@gmail.com, tkmpraveens@gmail.com"""

class Person(models.Model):
    first_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LastDone(models.Model):
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    not_done_reason = models.CharField(max_length=150, blank=True)

class Token(models.Model):
    token = models.CharField(max_length=150, blank=False)
    is_read = models.BooleanField(default=False)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

