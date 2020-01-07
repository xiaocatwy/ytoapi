#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: agent_login.py
@time: 2019/6/20 11:30 AM
@desc:
'''
import ujson
from sanic import Blueprint, response
from base import jinja
from conf import AGENT_COOKIE_TOKEN
from models.agent_do import AgentMerchant
login_agent_bp = Blueprint("login_agent")
from utils.cookie_util import set_cookies

# 定义登录函数
@login_agent_bp.route('/login_agent', methods=['GET', 'POST'])
async def login_agent(request):
    if request.method == 'GET':
        return jinja.render("agent/login.html", request)
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        # 用户名和密码长度，类型等验证，
        pwd = AgentMerchant().passwd(password)
        agent = AgentMerchant.get(AgentMerchant.phone == username, AgentMerchant.password == pwd)
        if agent:
            keys = ['show_id', 'phone', 'level', 'parent_id','username','agent_company']
            cookies = agent.to_dict(keys)
            cookies_json = set_cookies(AGENT_COOKIE_TOKEN, cookies)
            res = response.text(ujson.dumps({'status': 'success', 'code': 1}))
            res.cookies['agent_user'] = cookies_json
            res.cookies["agent_user"]["max-age"] = 3600
            return res
        else:
            res = response.text(ujson.dumps({'status':'failed','code':0,'info':'登录失败:用户名或密码错误'}))
            return res
    else:
        return jinja.render("agent/login.html", request, message="")



# 退出调用内置的登出函数，清除session
@login_agent_bp.route('/logout_agent')
async def logout_agent(request):
    return response.redirect('/login_agent', request)