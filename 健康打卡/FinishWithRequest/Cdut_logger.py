# -*- coding=utf-8 -*-
import logging
import logging.handlers
import os
'''
日志模块
'''
cur_path = os.path.dirname(os.path.abspath(__file__))

LOG_FILENAME = '{}/logs/running.log'.format(cur_path)

logger = logging.getLogger()


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
