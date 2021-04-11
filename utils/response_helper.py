#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
from decimal import Decimal

from django.http import HttpResponse


class ResState():
    """
    HTTP状态
    """
    HTTP_SUCCESS = 200
    HTTP_ERROR = 400
    SERVER_ERROR = 500
    ###提示信息全局变量
    ERROR_MSG = "操作失败"
    ERRPR_GET = "请求失败"
    ERRPR_LOGIN = "登录失败"
    ERROR_DB = "操作失败，请与管理员联系或稍后重试"
    ERROR_SYS = "系统错误，请与管理员联系或稍后重试"

class MyResponse(object):
    """
    适用于增删改查的返回
    """
    def __init__(self):
        self.status = 400
        self.msg = ResState.ERROR_MSG
        self.data = None

    def to_json(self):
        if self.status == 200:
            resp_data = json.dumps({"state": True, "data": self.data}, ensure_ascii=False,cls=DumpsEncoder)
        else:
            resp_data = json.dumps({"state": False,"code":self.status,"msg":str(self.msg)}, ensure_ascii=False, cls=DumpsEncoder)
        resp = HttpResponse(content=resp_data,status=200, content_type="application/json")
        return resp

    def to_json_msg(self,msg,status = None):
        self.msg=msg
        if status:
            self.status = status
        return self.to_json()

class DumpsEncoder(json.JSONEncoder):
    """
    格式化response中的日期
    """
    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, datetime.date):
                return obj.strftime("%Y-%m-%d")
            elif isinstance(obj, datetime.time):
                return obj.strftime("%H:%M:%S")
            elif isinstance(obj, Decimal):
                return float(obj)
            else:
                return obj
        except Exception as ex:
            logger.error("DumpsEncoder error by {0}".format(ex))