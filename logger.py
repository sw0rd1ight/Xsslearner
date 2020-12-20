# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 18:19
# @Author  : SwordLight
# @File    : logger.py

import logging
# logging.basicConfig(filename='valid_msg',filemode='w',level=logging.INFO)# 该只能设置logger的level handler的level默认为NOSET
logger=logging.getLogger('xsslearner')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(funcName)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('valid_msg.log')
fh.setLevel(logging.INFO)
f_formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(message)s')
fh.setFormatter(f_formatter)
logger.addHandler(fh)
