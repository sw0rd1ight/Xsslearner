# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 17:48
# @Author  : SwordLight
# @File    : analyse.py
import copy
import re
from pprint import pprint
from urllib.parse import urlparse

from config import HEADER, PAYLOAD_CHARS
from core.parser import HtmlParser
from core.requester import requester
from logger import logger
from utils import get_query_dict, get_url, gen_scout_str, gen_check_str, get_valid_paths

'''
1.找到需要替换的参数
2.生成随机字符替换参数来发起请求，拿到响应后得到上下文(属性、js、css
3.依据上下文进行尝试得到该上下文可用的用于达到执行js的符号，进行有效性评分
4.
'''

def analyse(url, GET, data=None, PATH=False):
    param_msg = {}  # 用于收集各个参数 对应的 context,position信息
    if GET:
        if PATH:  # 从url路径中取要替换的成分
            data = get_valid_paths(url)
        else:  # 从url参数中取要替换的成分
            url_parse_result = urlparse(
                url)  # ParseResult(scheme='http', netloc='192.168.1.46', path='/dvwa/vulnerabilities/xss_r/', params='', query='name=hi', fragment='')
            data = get_query_dict(url_parse_result.query)  # 参数键值对
            url = get_url(url, GET)  # request库中url和参数是分开传参的，故得到没有参数的url

    for param in data:
        scout_params = copy.deepcopy(data)
        scout_str = gen_scout_str()  # 特征字符串
        if PATH:  # 对于url路径参数
            repace_url = url  # 防止一个url被替换多次，故不改变原始url
            repace_url = repace_url.replace(param, scout_str)
            resp = requester(repace_url, headers=HEADER, data=None, GET=GET, delay=0, timeout=30)
        else:  # 对于get ,post参数
            scout_params[param] = scout_str
            resp = requester(url, data=scout_params, headers=HEADER, GET=GET, delay=0, timeout=30)
        text = resp.text
        parser=HtmlParser(target=scout_str)
        parser.feed(text)
        # print(text)
        # msg = []
        # positions = []  # 记录每个param出现的位置
        # for match in re.finditer(scout_str, text):
        #     positions.append(match.span())  # (31962, 31968)
        #
        # print(scout_str)
        #
        # parts = text.split(scout_str)
        # parts.remove(parts[0])
        #
        # for i in range(len(parts)):
        #     seed = parts[i].split('</')
        #     seed2 = parts[i].split(">")
        #     if len(seed) == 1:
        #         seed = parts[i].split('/>')
        #     print("seed:", len(seed), "\n", seed, )
        #     if seed[1].lower().find('script>') == 0:
        #         context = 'script'
        #     elif seed[1].lower().find('style>') == 0:
        #         context = 'css'
        #     elif '"' in seed2[0]:
        #         context = "attr"
        #     else:
        #         context = "html"
        #     msg.append({'position': positions[i], 'context': context})
        param_msg.update({param: parser.context})
    logger.info("param_msg:%s", str(param_msg))
    get_effective_chars(url, data, GET, param_msg)


# PATH 的话data会是一个list
def get_effective_chars(url, data, GET, msg):
    """根据上下文，然后得到上下文的重要字符，之后将特殊字符放到有效参数中，看看是否能够被找到"""
    scout_str = gen_scout_str()
    for key in msg:  # {'message': [{'positon': (31962, 31968), 'context': 'html'}], 'submit': []}
        for i in range(len(msg[key])):
            logger.info('msg[key][i][context]:%s', str(msg[key][i]))
            avoilable_char = []
            score = 0
            for check_char in PAYLOAD_CHARS[msg[key][i]['context']]:
                check_str = gen_check_str(scout_str, check_char)
                if isinstance(data, list):
                    repace_url = url  # 防止一个url被替换多次
                    repace_url = repace_url.replace(key, check_str)
                    logger.info("repace_url:%s", repace_url)
                    resp = requester(repace_url, data=None, GET=GET, headers=HEADER, delay=0, timeout=30)
                else:

                    check_params = copy.deepcopy(data)
                    check_params[key] = check_str
                    logger.info('check_params:%s', check_params)
                    resp = requester(url, data=check_params, GET=GET, headers=HEADER, delay=0, timeout=30)
                text = resp.text
                text_list=text.split('\n')
                # print(text)
                start_lineno = msg[key][i]['start_position'][0]
                try:
                    end_lineno=msg[key][i]['end_position'][0]
                except KeyError:
                    end_lineno=start_lineno
                target_zone='\n'.join(text_list[start_lineno-1:end_lineno])

                print("target_zone:",target_zone)
                res = target_zone.find(check_str)  # 由于字符串变量中的某些字符会转义，故无法用正则
                if res != -1:
                    avoilable_char.append(check_char)
                    score += 1
            msg[key][i].update({'avoilable_char': avoilable_char, 'score': score})

    # logger.info("msg:%s", str(msg))
    pprint(msg)


if __name__ == '__main__':
    data = {"city": 'hi', 'keyword': 'hi'}
    analyse('https://hr.sf-express.com/jobMainHandlerT/main/JAVA&9999', GET=True, data=None, PATH=True)
    # analyse('http://127.0.0.1/Less-1/?id=1', GET=True, data=None, PATH=False)
    # analyse('http://127.0.0.1/xss/xss_context.php?q=1&w=2&e=3&r=4&t=5', GET=True, data=None, PATH=False)
    # analyse('https://www.vivo.com.cn/search?q="CbL9bb',GET=True)