#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
logging配置
"""
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler

from django_demo import settings


def get_log_conf():

    # 定义日志输出格式 结束

    # 如果不存在定义的日志目录就创建一个
    logfile_dir = settings.LOGFILE_DIR  # log文件目录
    logfile_name = settings.LOGFILE_NAME # log文件名
    logfile_name_celery = settings.LOGFILE_NAME_CELERY # log文件名

    # 如果不存在定义的日志目录就创建一个
    if not os.path.isdir(logfile_dir):
        os.makedirs(logfile_dir, 755)

    # log文件的全路径
    logfile_path = os.path.join(logfile_dir, logfile_name)
    logfile_celery_path = os.path.join(logfile_dir, logfile_name_celery)

    # log配置字典
    LOGGING_DIC = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "%(asctime)s [%(levelname)s] thread_id:%(thread)d task_id:%(name)s (%(filename)s line:%(lineno)d): %(message)s\r",#logging会自动在每行log后面添加"\000"换行，windows下未自动换行
                'datefmt': "%Y-%m-%d %H:%M:%S",
            },
            'simple': {
                'format': '%(asctime)s [%(levelname)s] (%(filename)s line:%(lineno)d): %(message)s\r',
            },
        },
        'filters': {},
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',  # 打印到屏幕
                'formatter': 'simple'
            },
            'web_info_hander': {
                'level': 'DEBUG',
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',  # 支持多进程写日志
                'filename': logfile_path,  # 日志文件
                'maxBytes': 1024 * 1024 * 20,  # 日志大小 20M
                'backupCount': 20,
                'delay': True,  # If delay is true, file opening is deferred until the first call to emit
                'formatter': 'verbose',
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            },
            'celery_info_hander': {
                'level': 'DEBUG',
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',  # 支持多进程写日志
                'filename': logfile_celery_path,  # 日志文件
                'maxBytes': 1024 * 1024 * 20,  # 日志大小 20M
                'backupCount': 20,
                'delay': True,  # If delay is true, file opening is deferred until the first call to emit
                'formatter': 'verbose',
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            },
        },
        'loggers': {
            'default': {
                'handlers': [ 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': 'DEBUG',
                'propagate': True,  # 向上（更高level的logger）传递
            },
            'web_info': {
                'handlers': ['console', 'web_info_hander'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': 'DEBUG',
                'propagate': True,  # 向上（更高level的logger）传递
            },
            'celery_info': {
                'handlers': ['console', 'celery_info_hander'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': 'DEBUG',
                'propagate': True,  # 向上（更高level的logger）传递
            },
        },
    }
    return LOGGING_DIC


