# Generated by Django 3.1.7 on 2021-07-05 04:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AIModel',
            fields=[
                ('ai_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ai_name', models.CharField(default='AI_NAME', max_length=100)),
                ('ai_url', models.TextField(verbose_name='ai link url')),
                ('ai_status', models.IntegerField(default=0)),
                ('ai_description', models.TextField(verbose_name='ai description')),
                ('ai_type', models.IntegerField(default=0)),
                ('ai_credit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('ai_true_description', models.TextField(null=True, verbose_name='ai introduction')),
                ('ai_author', models.CharField(max_length=100, null=True)),
                ('ai_published', models.BooleanField(default=False)),
                ('ai_model_profile', models.TextField(null=True, verbose_name='ai model profile')),
                ('ai_usage', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ai_json', models.TextField(blank=True, verbose_name='ai req json data')),
                ('ai_result', models.TextField(blank=True, verbose_name='ai result json data')),
                ('ai_name', models.CharField(default='AI_NAME', max_length=100)),
                ('description', models.TextField(verbose_name='task description')),
                ('status', models.IntegerField(default=0)),
                ('time_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_done', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.IntegerField(default=0)),
                ('ai_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.aimodel')),
            ],
        ),
    ]
