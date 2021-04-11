from __future__ import absolute_import

# 日志配置
import logging.config
from utils.log_handler import get_log_conf
login_dict = get_log_conf()
logging.config.dictConfig(login_dict)
logger = logging.getLogger('web_info')
logcelery = logging.getLogger('celery_info')
# mysql配置
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()  # 使用pymysql代替mysqldb连接数据库



# 主线程中的全局redis链接池
# global_redis_pool的生命周期是Django主线程运行的生命周期
from utils.redis_pool import RedisPool
global_redis_pool = RedisPool()

# 主线程中的全局线程池
# global_thread_pool的生命周期是Django主线程运行的生命周期
from utils.thread_pool import ThreadPool
global_thread_pool = ThreadPool()

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
__all__ = ['celery_app']