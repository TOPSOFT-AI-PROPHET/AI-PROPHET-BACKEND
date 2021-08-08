# celeryconfig.py celery 配置文件

from datetime import timedelta

import djcelery
djcelery.setup_loader()

# 导入指定的任务模块
CELERY_IMPORTS = (
    'django_celery.tasks',
)


# 绑定默认队列为work_queue
CELERY_DEFAULT_QUEUE = 'work_queue'

# 有些情况可以防止死锁
CELERYD_FORCE_EXECV = True

#设置并发的worker数量
CELERYD_CONCURRENCY = 4

# 允许重试
CELERY_ACKS_LATE = True

#每个worker最多执行100个任务然后就被销毁，可以防止内存泄露(非常重要)
CELERYD_MAX_TASKS_PER_CHILD = 100

# 设置每一个任务的最大运行时间
CELERYD_TASK_TIME_LIMIT = 12 * 30
