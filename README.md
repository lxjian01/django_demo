1、常用操作
启动本地redis
/usr/local/redis-4.0.6/src/redis-server /usr/local/redis-4.0.6/redis.conf
VirutalEnv
pip install virtualenv
添加环境变量
mkdir /opt/venv
/usr/local/python3/bin/virtualenv -p /usr/bin/python3 /opt/venv/django_demo

日志组件在windows下需要安装pywin32==228



生成requirements.txt
1、生成架包依赖文件
pip freeze > requirements.txt
2、安装依赖架包
pip install -r requirements.txt
写日志windows下需要安装pypiwin32才能支持多进程写日志
pip install pypiwin32
需要指定环境变量
export DJANGO_ENV=dev


2、/etc/systemd/system/multi-user.target.wants/django-demo-gunicorn.service
[Unit]
Description=django demo gunicorn service
After=network.target
[Service]
User=root
Environment="DJANGO_ENV=dev"
Environment="PYTHONPATH=/opt/pyproject"
WorkingDirectory=/opt/pyproject/django_demo
ExecStart=/bin/sh -c 'source /opt/venv/django_demo/bin/activate && gunicorn -c gunicorn.py django_demo.wsgi:application'
LimitNOFILE=1024000
Restart=always
[Install]
WantedBy=multi-user.target


3、/etc/systemd/system/multi-user.target.wants/django-demo-celery-worker.service
[Unit]
Description=django demo celery worker service
After=network.target
[Service]
User=root
Environment="DJANGO_ENV=dev"
Environment="PYTHONPATH=/opt/pyproject"
WorkingDirectory=/opt/pyproject/django_demo
ExecStart=/bin/sh -c 'source /opt/venv/django_demo/bin/activate && celery -A django_demo --workdir=/opt/pyproject/django_demo worker --concurrency=2 --loglevel=INFO --logfile=/data/django-demo.celery.log'
LimitNOFILE=1024000
Restart=always
[Install]
WantedBy=multi-user.target


4、/etc/systemd/system/multi-user.target.wants/django-demo-celery-single-beat.service
[Unit]
Description=django-demo celery single-beat service
After=network.target
[Service]
User=root
Environment="DJANGO_ENV=dev"
Environment="SINGLE_BEAT_IDENTIFIER=celery-beat"
Environment="SINGLE_BEAT_REDIS_SERVER=redis://127.0.0.1:6379"
Environment="PYTHONPATH=/opt/pyproject"
WorkingDirectory=/opt/pyproject/django_demo
ExecStart=/bin/sh -c 'source /opt/venv/django_demo/bin/activate && single-beat celery -A django_demo --workdir=/opt/pyproject/django_demo beat'
LimitNOFILE=1024000
Restart=always
[Install]
WantedBy=multi-user.target