# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 16:12
# @Author  : SwordLight
# @File    : utils.py
import os
import random
import re
import tempfile
from urllib import parse

from config import defaultEditor
from core.colors import white, yellow
from log import setup_logger

logger = setup_logger(__name__)

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


def extractHeaders(headers):
    headers = headers.replace('\\n', '\n')
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers
def prompt(default=None):
    # try assigning default editor, if fails, use default
    editor = os.environ.get('EDITOR', defaultEditor)
    # create a temporary file and open it
    with tempfile.NamedTemporaryFile(mode='r+') as tmpfile:
        if default:  # if prompt should have some predefined text
            tmpfile.write(default)
            tmpfile.flush()
        child_pid = os.fork()
        is_child = child_pid == 0
        if is_child:
            # opens the file in the editor
            try:
                os.execvp(editor, [editor, tmpfile.name])
            except FileNotFoundError:
                logger.error('You don\'t have either a default $EDITOR \
value defined nor \'nano\' text editor')
                logger.info('Execute %s`export EDITOR=/pat/to/your/editor` \
%sthen run XSStrike again.\n\n' % (yellow,white))
                exit(1)
        else:
            os.waitpid(child_pid, 0)  # wait till the editor gets closed
            tmpfile.seek(0)
            return tmpfile.read().strip()  # read the file


if __name__ == "__main__":
    print(get_query_dict())
    print(get_query_str())
