# -*- coding: utf-8 -*-
# @Time    : 2020/6/28 9:56
# @Author  : SwordLight
# @File    : run.py
import argparse
import json
from core.analyse_by_parser import analyse
import log
from core.colors import red, white, end

logger = log.setup_logger()
# if __name__ == "__main__":

print('''%s
\tXSSLearner %sv1.0.0
%s''' % (red, white, end))
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True, help="Target url")
parser.add_argument("--path", help="Params in url")
# parser 参数中的双引号需要使用\转义
parser.add_argument("--data", help="Use Post method to send the data(dict)", type=str) #{\"searchFor\":\"hi\",\"goButton\":\"go\"}
args = parser.parse_args()


if args.data:  # 有额外的dict data 则是post
    url, GET, data, PATH = args.url, False, json.loads(args.data), False
elif args.path:  # 参数在path 一般是get
    url, GET, data, PATH = args.url, False, None, True
else:  # 不然则是get
    url, GET, data, PATH = args.url, True, None, False
analyse(url, GET, data, PATH)
