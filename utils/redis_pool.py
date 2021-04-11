#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from django_demo import settings, logger


class RedisPool(object):

    """
    redis池
    """

    def __init__(self,db=None):
        redis_cfg = settings.REDIS_CFG
        if db is None:
            db = redis_cfg['db']
        try:
            pool = redis.ConnectionPool(host=redis_cfg["host"], port=redis_cfg["port"],db = db, decode_responses=True)
            self.conn = redis.StrictRedis(connection_pool=pool, charset="utf-8")
            logger.info("Init redis pool ok.")
        except Exception as ex:
            logger.error("Init redis pool error by {0}.".format(ex))

    def __del__(self):
        self.conn.connection_pool.disconnect()
        logger.info("Redis pool closed.")


