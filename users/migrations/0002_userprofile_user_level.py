# Generated by Django 3.1.12 on 2021-07-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_level',
            field=models.IntegerField(default=0),
        ),
    ]
