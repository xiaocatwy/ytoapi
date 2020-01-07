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
from conf import AGENT_COOKIE_TOKEN
import logging
import traceback


def check_agent_authorization(request):
    '''校验cookie'''
    flag = True
    try:
        cookies = request.cookies.get('agent_user', '')
        if not cookies:
            flag = False
        else:
            agent_user = get_cookies(AGENT_COOKIE_TOKEN, cookies)
            setattr(request.app, 'agent_user', agent_user)
    except:
        logging.error(traceback.format_exc())
        flag = False
    return flag

def agent_authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = check_agent_authorization(request)

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                from sanic import response
                return response.redirect('/login_agent')
        return decorated_function
    return decorator