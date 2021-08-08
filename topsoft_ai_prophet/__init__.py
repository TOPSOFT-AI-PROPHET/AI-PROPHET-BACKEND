# -*- coding: utf-8 -*- celery 配置文件
from __future__ import absolute_import, unicode_literals

from .celery import app as celery_ap

import pymysql


pymysql.install_as_MySQLdb()

__all__ = ['celery_app']