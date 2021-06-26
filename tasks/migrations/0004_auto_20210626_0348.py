# Generated by Django 3.2 on 2021-06-26 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_aimodel_ai_introduction'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='ai_author',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='ai_model_profile',
            field=models.TextField(null=True, verbose_name='ai model profile'),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='ai_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='ai_usage',
            field=models.IntegerField(default=0),
        ),
    ]
