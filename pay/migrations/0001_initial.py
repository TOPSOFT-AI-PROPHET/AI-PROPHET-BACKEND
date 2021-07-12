# Generated by Django 3.1.12 on 2021-07-11 05:55

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('method', models.IntegerField(default=0)),
                ('order', models.CharField(max_length=1025)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('done_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
