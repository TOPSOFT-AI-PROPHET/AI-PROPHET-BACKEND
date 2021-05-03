from django.db import models
from users.models import UserProfile
from django.utils import timezone

class AIModel(models.Model):
    ai_id = models.BigAutoField(primary_key=True)
    ai_name = models.CharField(max_length=100)
    ai_url = models.TextField(verbose_name='ai link url')
    ai_status = models.IntegerField(default=0)
    ai_description = models.TextField(verbose_name='ai description')
    ai_type = models.IntegerField(default=0)
    ai_credit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    ai_introduction = models.TextField(verbose_name= 'ai introduction', null = True)
    ai_true_description = models.CharField(max_length=255)

class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True) 
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE,default=1)
    ai_id = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    ai_json = models.TextField(verbose_name='ai req json data', blank=True)
    ai_result = models.TextField(verbose_name='ai result json data', blank=True)
    ai_name = models.CharField(max_length=100)
    description = models.TextField(verbose_name='task description')
    status = models.IntegerField(default=0)
    time_start = models.DateTimeField(default=timezone.now)
    time_done = models.DateTimeField(blank=True, null=True)
    is_delete = models.IntegerField(default=0)