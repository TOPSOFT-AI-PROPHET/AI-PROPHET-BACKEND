# Generated by Django 3.1.12 on 2021-07-18 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_aimodel_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aimodel',
            old_name='UserProfile',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='aimodel',
            name='ai_author',
        ),
    ]
