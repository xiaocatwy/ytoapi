#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: cookie_util.py
@time: 2019/7/6 2:51 PM
@desc:
'''
from cryptography.fernet import Fernet
from sanic.request import json_loads
from sanic.response import json_dumps


def set_cookies(token,cookies):
    '''
    加密cookies
    :param token:
    :param cookies:
    :return:
    '''
    f = Fernet(token)
    cookies_json = json_dumps(cookies)
    token = f.encrypt(cookies_json.encode())
    cookies_json = token.decode()
    return cookies_json


def get_cookies(token, cookies):
    '''
    解密cookies
    :param token:
    :param cookies:
    :return:
    '''
    token = token.decode('utf-8')
    f = Fernet(token)
    cookie_json = f.decrypt(cookies.encode()).decode()
    cookies_data = json_loads(cookie_json)
    return cookies_data

