# Generated by Django 3.2.23 on 2023-12-27 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_is_acitve'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='is_acitve',
            new_name='is_active',
        ),
    ]
