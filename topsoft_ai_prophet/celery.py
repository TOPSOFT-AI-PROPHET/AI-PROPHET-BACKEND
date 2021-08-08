# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery

# 只要是想在自己的脚本中访问Django的数据库等文件就必须配置Django的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topsoft_ai_prophet.settings')

# app名字
app = Celery('topsoft_ai_prophet')

# 配置celery
class Config:
    BROKER_URL = 'redis://127.0.0.1:6379'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'

app.config_from_object(Config)
# 到各个APP里自动发现tasks.py文件
app.autodiscover_tasks()
