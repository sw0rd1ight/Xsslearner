# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 16:12
# @Author  : SwordLight
# @File    : utils.py
import random
from urllib import parse


def gen_scout_str(length=6):
    """产生指定长度的探子字符串"""
    chars = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789"
    scout = ''
    for i in range(length):
        scout += random.choice(chars)
    return scout


def get_query_dict(query_str='name=hi&age=20'):
    # name=hi&age=20  todo 之后 参数需要兼容 \  \\这种格式的
    parts = query_str.split('&')
    query_dict = {}
    for part in parts:
        key, value = part.split('=')
        query_dict.update({key: value})
    return query_dict


def get_query_str(query_dict={'name': 'hi', 'age': '20'}):
    query_str = ""
    for k, v in query_dict.items():
        query_str += k + "=" + v + "&"
    return query_str[:-1]


def gen_check_str(scout_str, char):
    idx = random.randint(1, len(scout_str)-1)
    check_str = scout_str[:idx] + char + scout_str[idx:]
    return check_str


def get_url(url, GET):
    if GET:
        return url.split('?')[0]
    else:
        return url


def get_valid_paths(url):
    path = parse.urlparse(url).path
    print("valid_paths:", path)
    paths = path.split(r'/')
    paths = [i for i in paths if i != '']
    return paths



if __name__ == "__main__":
    print(get_query_dict())
    print(get_query_str())
