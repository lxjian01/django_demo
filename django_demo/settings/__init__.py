# 根据环境变量导入不同设置文件
# 如果环境变量中存在 ENV（具体值可行自定义）则判定为生产环境导入生产环境设置
# 否则则判定为开发环境导入开发环境设置
import os
env = os.environ.get('DJANGO_ENV', "dev")
if env == "prod":
    from .prod import *
elif env == "test":
    from .test import *
else:
    from .dev import *