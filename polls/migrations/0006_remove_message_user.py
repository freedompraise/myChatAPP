# Generated by Django 4.0.3 on 2022-03-30 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_remove_topic_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
    ]
