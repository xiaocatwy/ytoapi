#!/usr/bin/env python
# encoding: utf-8

'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: authorized.py
@time: 2019/6/20 5:59 PM
@desc:
'''
from functools import wraps
from utils.cookie_util import get_cookies
from conf import COOKIE_TOKEN
import logging
import traceback

def check_admin_authorization(request):
    '''校验cookie'''
    flag = True
    try:
        cookies = request.cookies.get('user', '')
        if not cookies:
            flag = False
        else:
            user = get_cookies(COOKIE_TOKEN,cookies)
            setattr(request.app, 'user', user)
        if not hasattr(request.app,'user'):
            flag = False
    except:
        logging.error(traceback.format_exc())
        flag = False
    return flag

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = check_admin_authorization(request)
            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                from sanic import response
                return response.redirect('/login')
        return decorated_function
    return decorator
