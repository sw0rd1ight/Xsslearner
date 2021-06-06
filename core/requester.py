# -*- coding: utf-8 -*-
# @Time    : 2020/6/21 16:03
# @Author  : SwordLight
# @File    : requester.py
import time
import requests

import config


def requester(url,data,headers,GET,delay,timeout=60):
    time.sleep(delay)
    if GET:
        resp=requests.get(url=url,params=data,headers=headers,timeout=timeout, proxies=config.PROXIES)
    else:
        resp=requests.post(url=url,data=data,headers=headers,timeout=timeout, proxies=config.PROXIES)
    return resp




