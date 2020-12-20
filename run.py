# -*- coding: utf-8 -*-
# @Time    : 2020/6/28 9:56
# @Author  : SwordLight
# @File    : run.py
import argparse
import json
from core.analyse import analyse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, help="Target url")
    parser.add_argument("--path", help="Params in url")
    # parser 参数中的双引号需要使用\转义
    parser.add_argument("--data", help="Use Post method to send the data(dict)", type=str) #{\"searchFor\":\"hi\",\"goButton\":\"go\"}
    args = parser.parse_args()
    print(args,args.data)

    if args.data:  # 有额外的dict data 则是post
        url, GET, data, PATH = args.url, False, json.loads(args.data), False
    elif args.path:  # 参数在path 一般是get
        url, GET, data, PATH = args.url, False, None, True
    else:  # 不然则是get
        url, GET, data, PATH = args.url, True, None, False
    analyse(url, GET, data, PATH)
