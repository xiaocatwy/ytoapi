#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: base.py
@time: 2019/3/6 12:01 PM
@desc:
'''
import random
from sanic import Sanic
app = Sanic(__name__)

app_setting = {
    'REQUEST_BUFFER_QUEUE_SIZE':512,
    'KEEP_ALIVE':False,
    'KEEP_ALIVE_TIMEOUT':5,
    'ACCESS_LOG':True
}
app.config.update(app_setting)

# agent_app = Sanic(__name__)

from sanic_jinja2 import SanicJinja2
jinja = SanicJinja2(app)
# agent_jinja = SanicJinja2(agent_app)

from sanic_auth import Auth
auth = Auth(app)
app.config.AUTH_LOGIN_ENDPOINT = 'login11.html'

# agent_auth = Auth(app)
# agent_app.config.AUTH_LOGIN_ENDPOINT = 'login.html'

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

@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    pass
    # await session.open(request)

@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    pass
    # await session.save(request, response)

# @agent_app.middleware('request')
# async def add_session_to_request(request):
#     pass
#
# @agent_app.middleware('response')
# async def save_session(request, response):
#     pass

