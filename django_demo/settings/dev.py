from datetime import timedelta

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Celery application definition
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = "/data/django-demo-celery.log"
CELERYBEAT_LOG_FILE = "/data/django-demo-celery-beat.log"

# 这里是定时任务的配置
CELERY_BEAT_SCHEDULE = {
    'task_method': {  # 随便起的名字
        'task': 'user.tasks.test_celery',  # app 下的tasks.py文件中的方法名
        'schedule': timedelta(seconds=1),  # 名字为task_method的定时任务, 每10秒执行一次
    },
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   #  指定数据库驱动
        'NAME': 'django_demo',   #  指定的数据库名
        'USER': 'devops',   #  数据库登录的用户名
        'PASSWORD': 'devops',  #  登录数据库的密码
        'HOST': '127.0.0.1',
        'PORT': '3306',   #  数据库服务器端口，mysql默认为3306
    }
}


# redis在django中的配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}
# session的存储配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 设置session失效时间,单位为秒
SESSION_COOKIE_AGE = 60*5

### redis配置
REDIS_CFG = {"host": "127.0.0.1", "port": 6379,"db":0}