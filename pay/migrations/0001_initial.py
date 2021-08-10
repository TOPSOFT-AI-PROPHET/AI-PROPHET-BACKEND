# Generated by Django 3.1.7 on 2021-08-08 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cdklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdk', models.CharField(max_length=1025)),
                ('amount', models.IntegerField(default=0)),
                ('is_used', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('status', models.IntegerField(default=0)),
                ('method', models.TextField(null=True, verbose_name='method')),
                ('order', models.CharField(max_length=1025)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('done_time', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
