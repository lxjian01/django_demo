#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import multiprocessing

bind = '0.0.0.0:8000'   #绑定的ip及端口号
backlog = 512                #监听队列
chdir = '/opt/django_demo'  #你项目的根目录,比如我的app.py文件在/home/ubuntu/app目录下，就填写'/home/ubuntu/web'
timeout = 30      #超时
proc_name = 'django-demo.gunicorn.proc'
workers = multiprocessing.cpu_count()*2 + 1   #进程数
worker_class = "gevent"
max_requests = 20480    #设置一个进程处理完max_requests次请求后自动重启,就是设置这个可以预防内存泄漏，如果不设置的话，则进程不会自动重启

loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s|%(p)s|%(h)s|"%(r)s"|%(s)s|%(L)s|%(b)s|%(f)s|"%(a)s"'    #设置gunicorn访问日志格式，错误日志无法设置
accesslog = "/data/django-demo.gunicorn.access.log"      #访问日志文件
errorlog = "/data/django-demo.gunicorn.error.log"        #错误日志文件