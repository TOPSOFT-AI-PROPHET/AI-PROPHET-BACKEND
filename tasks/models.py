from django.utils import timezone
from users.models import UserProfile
from django.db import models


class AIModel(models.Model):
    ai_id = models.BigAutoField(primary_key=True)
    ai_name = models.CharField(max_length=100, default="AI_NAME")
    ai_url = models.TextField(verbose_name='ai link url')
    # 0-100 （-1 means failure)
    ai_status = models.IntegerField(default=0)
    # descibe parameters for developers
    ai_description = models.TextField(verbose_name='ai description')
    # 0 decision tree....
    ai_type = models.IntegerField(default=0)
    ai_credit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    # general description about this model for normal users 
    ai_true_description = models.TextField(verbose_name= 'ai introduction', null = True)
    ai_author = models.CharField(max_length=100, null = True)
    # 0=not_published, 1=published
    ai_published = models.IntegerField(default=0)
    ai_model_profile = models.TextField(verbose_name= 'ai model profile', null = True)
    # how many times is this model used
    ai_usage = models.IntegerField(default=0)
    # how many training materials are passed into this model to train
    ai_training_material_count = models.IntegerField(default=0)
    # 0=frozen 1=not_frozen 
    ai_frozen = models.IntegerField(default=0)
    # foreign key
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, default='')
    


class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, default=1)
    ai_id = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    # kinds of training materials
    ai_json = models.TextField(verbose_name='ai req json data', blank=True)
    ai_result = models.TextField(
        verbose_name='ai result json data', blank=True)
    ai_name = models.CharField(max_length=100, default="AI_NAME")
    # 备注
    description = models.TextField(verbose_name='task description')
    status = models.IntegerField(default=0)
    time_start = models.DateTimeField(default=timezone.now)
    time_done = models.DateTimeField(blank=True, null=True)
    is_delete = models.IntegerField(default=0)
