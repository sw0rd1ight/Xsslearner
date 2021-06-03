# -*- coding: utf-8 -*-
# @Time    : 2020/6/21 15:07
# @Author  : SwordLight
# @File    : config.py
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Cookie": "security=low; PHPSESSID=4vohc8becnbkgusij602lm1ro1",
    "Connection": "close"}

PAYLOAD_CHARS = {"script": ["<", ">", "'", '"'], "attr": ["<>", '"', "."], "html": ["<>", "<", ">"],
                 "css": ["expression", "."], "comment": ["-->", "--!>"]}

PAYLOAD_CHARS_ = {
    "script": {"breaker": {";": 10,'"':5,"'":5},
               "exploiter": {".":1, "()":1, "[]":1, "/":1, "=":1}},
    "html": {"breaker": {">": 10, "</": 10},
             "exploiter": {".":1, "()":1, "[]":1, "/":1, "=":1}},
    "attr": {"breaker": {"'": 10, '"': 10},
             "exploiter": {".":1, "()":1, "[]":1, "/":1, "=":1}},
    "css": {"breaker": {"expression(": 10,"'":10,'"':10}, "exploiter": { "[]":1, "/":1, "=":1}},
    "comment": {"breaker": {"-->": 10, "--!>": 10},
                "exploiter": {".":1, "()":1, "[]":1, "/":1, "=":1}},
}




BAD_TAGS = ('iframe', 'title', 'textarea', 'noembed',
            'template', 'noscript')