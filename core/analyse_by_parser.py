# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 17:48
# @Author  : SwordLight
# @File    : analyse.py
import copy
from pprint import pprint
from urllib.parse import urlparse

from config import HEADER, PAYLOAD_CHARS, PAYLOAD_CHARS_
from core.parser import HtmlParser
from core.requester import requester
import log
from utils import get_query_dict, get_url, gen_scout_str, gen_check_str, get_valid_paths

'''
1.找到需要替换的参数
2.生成随机字符替换参数来发起请求，拿到响应后得到上下文(属性、js、css
3.依据上下文进行尝试得到该上下文可用的用于达到执行js的符号，进行有效性评分
4.
'''

logger = log.setup_logger(__name__)


def analyse(url, GET, data=None, PATH=False):
    param_msg = {}  # 用于收集各个参数 对应的 context,position信息
    if GET:
        if PATH:  # 从url路径中取要替换的成分
            data = get_valid_paths(url)
        else:  # 从url参数中取要替换的成分
            url_parse_result = urlparse(
                url)  # ParseResult(scheme='http', netloc='192.168.1.46', path='/dvwa/vulnerabilities/xss_r/', params='', query='name=hi', fragment='')
            query = url_parse_result.query
            if query == "":
                query = url_parse_result.path.split("/")[-1]
            data = get_query_dict(query)  # 参数键值对
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
        parser = HtmlParser(target=scout_str)
        parser.feed(text)
        logger.info("参数{}的上下文：{}".format(param, parser.context))
        logger.red_line()

        param_msg.update({param: parser.context})
    # logger.info("param_msg:%s" % str(param_msg))
    get_effective_chars(url, data, GET, param_msg)


def estimate_payload_char(payload_chars, chars_type, url, data, test_param, context_info, GET):
    '''

    :param payload_chars: 用于尝试的payload字符
    :param chars_type:区分是breakers 或  exploiter
    :param url:
    :param data: 可以替换的参数 对于路径替换的情况为list,对于参数替换的情况为dict
    :param test_param: 当前被测试的参数
    :param context_info: 当前被测试参数在resp中的上下艾文信息
    :param GET: True则为 get请求方法
    :return:
    '''
    estimate_res = {"avail_chars": [], "sore": 0, "output_zone": ""}
    for char in payload_chars:
        scout_str = gen_scout_str()
        check_str = gen_check_str(scout_str, char)
        if isinstance(data, list):  # 路径处理
            repace_url = url  # 防止一个url被替换多次
            repace_url = repace_url.replace(test_param, check_str)
            resp = requester(repace_url, data=None, GET=GET, headers=HEADER, delay=0, timeout=30)
        else:
            check_params = copy.deepcopy(data)
            check_params[test_param] = check_str
            resp = requester(url, data=check_params, GET=GET, headers=HEADER, delay=0, timeout=30)
        text = resp.text
        text_list = text.split('\n')
        start_lineno = context_info['start_position'][0]
        try:
            end_lineno = context_info['end_position'][0]
        except KeyError:
            end_lineno = start_lineno
        output_zone = '\n'.join(text_list[start_lineno - 1:end_lineno])
        res = output_zone.find(check_str)  # 由于字符串变量中的某些字符会转义，故无法用正则
        if res != -1:
            estimate_res["avail_chars"].append(char)
            estimate_res["sore"] += PAYLOAD_CHARS_[context_info["context"]][chars_type][char]
            estimate_res["output_zone"] = output_zone  # 保存最后一个可行的回显位置
    return estimate_res


# PATH 的话data会是一个list
def get_effective_chars(url, data, GET, msg):
    """根据上下文，然后得到上下文的重要字符，之后将特殊字符放到有效参数中，看看是否能够被找到"""
    for key in msg:  # {'message': [{'positon': (31962, 31968), 'context': 'html'}], 'submit': []}
        logger.run("评估参数:{}".format(key))
        logger.info("输出点个数:{}".format(len(msg[key])))

        for i in range(len(msg[key])):
            logger.run("评估第{}个输出点".format(i + 1))
            # {'avail_chars': ['.'], 'sore': 1, 'output_zone': '    <!--\n        this is comment\n        dbUfe.D        -->'}
            est_breaker_res = estimate_payload_char(PAYLOAD_CHARS_[msg[key][i]['context']]["breaker"], "breaker", url,
                                                    data, key, msg[key][i], GET)
            est_exploiter_res = estimate_payload_char(PAYLOAD_CHARS_[msg[key][i]['context']]["exploiter"], "exploiter",
                                                      url, data, key, msg[key][i], GET)
            msg[key][i].update({'breakers': est_breaker_res["avail_chars"],
                                "exploiter": est_exploiter_res["avail_chars"],
                                'sore': est_breaker_res["sore"] + est_exploiter_res["sore"],
                                "output_zone": est_breaker_res["output_zone"]})
            logger.info("上下文: {}".format(msg[key][i]["context"]))
            logger.info("相关html标签: {}".format(msg[key][i]["tag"]))
            logger.info("相关特殊标记: {}".format(msg[key][i]["sp"]))
            logger.vuln("breakers得分： {}".format(est_breaker_res["sore"]))
            logger.info("可用breakers: {}".format(est_breaker_res["avail_chars"]))
            logger.vuln("exploiter得分： {}".format(est_exploiter_res["sore"]))
            logger.info("可用exploiter: {}".format(est_exploiter_res["avail_chars"]))
            logger.info("输出点信息: {}".format(est_breaker_res["output_zone"]))
            logger.red_line(amount=60)
        logger.red_line()

    # pprint(msg)
    # logger.good(str(msg))


if __name__ == '__main__':
    analyse('http://127.0.0.1/xss/xss_context.php?q=1&w=2&e=3&r=4&t=5', GET=True, data=None, PATH=False)
