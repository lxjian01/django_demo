import threading
from concurrent.futures.thread import ThreadPoolExecutor

from django_demo import logger, settings


class ThreadPool(object):
    """
    线程池
    """
    def __init__(self):
        # 线程池
        thread_num = settings.THREAD_POOL_EXECUTOR_NUM
        self.executor = ThreadPoolExecutor(thread_num)
        # 用于存储每个项目批量任务的期程
        self.future_dict = {}
        # 全局锁
        self.lock = threading.Lock()
        logger.info("Init thread pool ok.")

    # 检查某个项目是否有正在运行的批量任务
    def is_project_thread_running(self, project_id):
        future = self.future_dict.get(project_id, None)
        if future and future.running():
            # 存在正在运行的批量任务
            return True
        return False

    # 展示所有的异步任务
    def check_future(self):
        data = {}
        for project_id, future in self.future_dict.items():
            data[project_id] = future.running()
        return data

    def __del__(self):
        self.executor.shutdown()
        logger.info("Thread pool closed.")