# Generated by Django 3.1.7 on 2021-04-12 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_image_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image_uuid',
            field=models.CharField(blank=True, max_length=255, verbose_name='uuid'),
        ),
    ]