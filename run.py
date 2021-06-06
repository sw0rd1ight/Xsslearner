# -*- coding: utf-8 -*-
# @Time    : 2020/6/28 9:56
# @Author  : SwordLight
# @File    : run.py
import argparse
import json

import config
import log
from config import HEADER
from core.analyse_by_parser import analyse
from core.colors import red, white, end
from utils import extractHeaders, prompt

logger = log.setup_logger()

print('''%s
\tXSSLearner %sv1.0.0
%s''' % (red, white, end))
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True, help="Target url")
parser.add_argument("--path", help="Params in url",action='store_true')
# parser 参数中的双引号需要使用\转义
parser.add_argument("--data", help="Use post method to send the data(dict)", type=str) #{\"searchFor\":\"hi\",\"goButton\":\"go\"}
parser.add_argument('--header', help='Add header',
                    dest='add_header', nargs='?', const=True)
parser.add_argument('--proxy', help='use prox(y|ies)',
                    dest='proxy', action='store_false')
args = parser.parse_args()


if type(args.add_header) == bool:
    header = extractHeaders(prompt())
elif type(args.add_header) == str:
    header = extractHeaders(args.add_header)
else:
    header=HEADER
# 代理
if not args.proxy:
    config.PROXIES = {}

if args.data:  # 有额外的dict data 则是post
    url, GET, data, PATH = args.url, False, json.loads(args.data), False
elif args.path:  # 参数在path 一般是get
    url, GET, data, PATH = args.url, True, None, True
else:  # 不然则是get
    url, GET, data, PATH = args.url, True, None, False
analyse(url, GET, data, PATH,header)
