#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: __init__.py.py
@time: 2019/3/6 11:45 AM
@desc:
'''
from __future__ import absolute_import, division, print_function

from sanic.response import json
from functools import wraps

def check_request_for_authorization_status(request):
    # Note: Define your check, for instance cookie, session.
    flag = True
    return flag

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator


from .page import Paginator
PAGE_SIZE = 10


def get_page_url(request, page=1, form_id=None):
    """参数解析
    :page 页号
    :form_id
    """
    if form_id:
        return "javascript:goto_page('%s',%s);" % (form_id.strip(), page)
    path = request.path
    req_string = request.query_string
    def _page_url(p=page,form_id=form_id):
        return path + '?page={0}&'.format(p)+req_string
    return _page_url

def get_page_data(request,query):
    '''
    分页函数
    :param query:
    :param page_size:
    :return:
    '''
    _page_size = request.args.get("page_size",'')
    if not _page_size:
        page_size = PAGE_SIZE
    else:
        page_size = int(_page_size)
    page = int(request.args.get("page", 1))
    offset = (page-1) * page_size
    result = query.limit(page_size).offset(offset)
    page_data = Paginator(get_page_url(request), page, query.count(), page_size)
    page_data.result = result
    return page_data

import random

def get_id_by_show_id(showId):
    '''
    根据showid获取真实id值
    :param showId: type string 自动增长列id值
    :return:
    '''
    i = showId[len(showId) - 1]
    j = showId[0:len(showId) - 1]
    k = (int(j) - int(i) - 10000) / int(i)
    return k

def set_show_id_by_id(id):
    '''
    设置showid
    :param id: 真实id
    :return:
    '''
    a = random.randint(1, 9)
    b = a * int(id) + 10000 + a
    j = str(b) + str(a)
    return j

import functools
from sanic import response

def login_required(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        return method(self, *args, **kwargs)
        # user = self.cookies.get("user")
        # print(user)
        # if user:
        #     return method(self, *args, **kwargs)
        # else:
        #     return response.redirect('/login2.html')
    return wrapper


config = {
    "YTO":"YTO",
    "UrlOrder":"http://service.yto56.net.cn/CommonOrderModeBPlusServlet.action",
    "UrlWeight":"http://116.228.115.225:6183/3rdface/open-service/persist/weight",
    "ClientID":"K11122126",
    "ClientSec":"D570nY8Y",
    "WeightSec":"7d35f6f98e025b85b75c283260af5d09"
}
import hashlib
import base64

def signatral(xml_body, client_sec):
    '''
    签名
    :param xml_body:
    :param client_sec:
    :return:
    '''
    m = hashlib.md5()
    data= xml_body+client_sec
    if isinstance(xml_body,bytes):
        m.update(data.encode('utf-8'))
    else:
        m.update(data.encode('utf-8'))
    str_result = base64.b64encode(m.digest())
    return str_result

sender = {"name":"", "mobile":"", "prov":"","city":"", "address":""}
recive = {"name":"", "mobile":"", "prov":"", "city":"", "address":""}
item = {"itemName":"", "number":"", "itemValue":""}

custom_root = 'RequestOrder'
from dicttoxml import dicttoxml

