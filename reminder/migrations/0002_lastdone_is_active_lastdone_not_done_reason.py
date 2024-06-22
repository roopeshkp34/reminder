# Generated by Django 4.2.13 on 2024-06-22 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lastdone',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lastdone',
            name='not_done_reason',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
