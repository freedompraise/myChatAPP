# Generated by Django 4.0.3 on 2022-03-30 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_message_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='name',
        ),
    ]