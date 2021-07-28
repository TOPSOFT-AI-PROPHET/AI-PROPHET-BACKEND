from django.db import models
from users.models import UserProfile
from django.utils import timezone
import uuid

class Transaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4) # for cdk
    status = models.IntegerField(default=0) # 充值结果
    method = models.TextField(verbose_name='method', null=True) # 充值方式
    order = models.CharField(max_length=1025) # 充值的备注？
    credit = models.DecimalField(max_digits=20, decimal_places=2)
    create_time = models.DateTimeField(default=timezone.now)
    done_time = models.DateTimeField(blank=True, null=True)

class Cdklist(models.Model):
    cdk = models.CharField(max_length=1025)
    amount = models.IntegerField(default=0)
    is_used = models.IntegerField(default=0)