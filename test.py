# # -*- coding: utf-8 -*-
# # @Time    : 2020/6/19 15:57
# # @Author  : SwordLight
# # @File    : test.py
# import re
# import random
# import requests
# from urllib import parse
# from utils import get_query_dict, gen_scout_str, get_query_str
# from urllib.parse import urlsplit,urlparse
# import copy
#
#
#
# def gen_check_str(scout_str, char):
#     idx = random.randint(0,len(scout_str))
#     check_str = scout_str[:idx] + char + scout_str[idx:]
#     return check_str
#
# def get_effective_chars(url_dict, query_dict, msg):
#     """根据上下文，然后得到上下文的重要字符，之后将特殊字符放到有效参数总，看看是否能够被找到"""
#
#     scout_str = 'v12R2U'
#     for key in msg:  # {'message': [{'positon': (31962, 31968), 'context': 'html'}], 'submit': []}
#
#         for i in range(len(msg[key])):
#             print('msg[key][i][context]:',msg[key][i])
#             avoilable_char = []
#             score = 0
#             for check_char in payload[msg[key][i]['context']]:
#
#                 check_str = gen_check_str(scout_str, check_char)
#                 quote_check_str=parse.quote(check_str)
#                 print("check_str:",check_str)
#                 query_dict[key] = quote_check_str
#                 query_str = get_query_str(query_dict)
#                 print('query_str',query_str)
#                 test_url_dict=url_dict._replace(query=query_str)
#                 check_url = test_url_dict.geturl()
#                 print("check_url:",check_url)
#                 resp = requests.get(check_url, headers=headers)
#                 text = resp.text
#                 start = msg[key][i]['position'][0] - 10
#                 try:
#                     end = msg[key][i + 1]['position'][1] + 10
#                 except IndexError:
#                     end = len(text)
#                 # print(text[start:end])
#                 # partten=eval(r''+check_str)
#
#                 res=re.search(check_str,text[start:end])
#                 #res = text[start:end].find(check_str) # 由于字符串变量中的某些字符会转义，故无法用正则
#                 if res is not None:
#                     print('res:',res)
#                     avoilable_char.append(check_char)
#                     score += 1
#             msg[key][i].update({'avoilable_char': avoilable_char, 'score': score})
#
#
#     print(msg)
#
#
# test_url1="http://192.168.1.46/test.php?s=1"
# test_url1="http://www.zhongdinggroup.cn/cn/search.aspx?gp=100&sear_key=hi"
# url_dict=urlparse(test_url1) #ParseResult(scheme='http', netloc='192.168.1.46', path='/dvwa/vulnerabilities/xss_r/', params='', query='name=hi', fragment='')
# query_dict=get_query_dict(url_dict.query) # 参数键值对
#
# headers={
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
# "Cookie":"security=low; PHPSESSID=4vohc8becnbkgusij602lm1ro1" ,
# "Connection": "close"}
#
# payload={"script":["<",">"],"attr":["<>",'"',"."],"html":["<>","<",">"],"css":["expression","."]}
# k_context={}
# for k in query_dict:
#     test_query_dict=copy.deepcopy(query_dict)
#     scout_str = 'v12R2U'
#     test_query_dict[k]=scout_str
#     query_str=get_query_str(test_query_dict)
#     new_url_dict=url_dict._replace(query=query_str)
#     scout_url=new_url_dict.geturl()
#     print("scout_url:",scout_url)
#     res=requests.get(scout_url,headers=headers)
#     text=res.text
#
#     msg = []
#     positions=[]
#
#     for match in re.finditer(scout_str,text):
#         positions.append(match.span())# (31962, 31968)
#
#     parts=text.split(scout_str)
#
#     parts.remove(parts[0])
#     print('len(parts):',len(parts))
#
#     for i in range(len(parts)):
#         seed=parts[i].split('</')
#         seed2 = parts[i].split(">")
#         context=''
#         if  seed[1].lower().find('script>')==0:
#             context='script'
#         elif seed[1].lower().find('style>')==0:
#             context='css'
#         elif '"' in seed2[0] :
#             context="attr"
#         else:
#             context="html"
#         msg.append({'position':positions[i],'context':context})
#     k_context.update({k:msg})
#
# print(k_context)
# get_effective_chars(url_dict,query_dict,k_context)
#
#
#
#
#
#
#
#
# # print(url_dict)
#
#
import requests

resp=requests.get(r'https://www.vivo.com.cn/search?q="CbL9bb')
print(resp.text)
