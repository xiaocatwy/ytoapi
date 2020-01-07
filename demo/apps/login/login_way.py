#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: advertise_do.py
@time: 2019/6/20 11:30 AM
@desc:
'''
import time
import uuid
import ujson

from sanic import Blueprint, response
from sanic.response import text
import hashlib
from base import auth
from middleware.authorized import authorized
from models.money import Balance
from models.user import Users
from base import jinja
import hashlib
from conf import COOKIE_TOKEN
login_bp = Blueprint("login")

from utils.cookie_util import set_cookies

# 定义登录函数
@login_bp.route('/login', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        #用户名和密码长度，类型等验证，
        pwd = Users().passwd(password)
        admin = Users.get(Users.phone == username, Users.password == pwd)
        if admin:
            keys = ['show_id','username','phone','is_admin','level','id','agent_id']
            cookies = admin.to_dict(keys)
            cookies_json =set_cookies(COOKIE_TOKEN,cookies)
            res = response.text(ujson.dumps({'login':'success','code':1}))
            res.cookies['user'] = cookies_json
            res.cookies["user"]["max-age"] = 36000
            return res
        else:
            res = response.text(ujson.dumps({'login': 'fail', 'code': 0,'info':'登录失败:用户名或密码错误'}))
            return res
    else:
        return jinja.render("admin/login.html", request, message="")


# 退出调用内置的登出函数，清除session
@login_bp.route('/logout')
@authorized()
async def logout(request):
    response = jinja.render("admin/login.html", request)
    del response.cookies["user"]
    return response


# 注册
@login_bp.route('/change_pwd', methods=['GET', 'POST'])
@login_bp.route('/register', methods=['GET', 'POST'])
async def user_register(request):
    if request.method == 'POST':
        name = request.form.get('name', '')
        phone = request.form.get('username', '')
        password = request.form.get('pwd', '')
        pwd = Users().passwd(password)
        code = request.form.get('user_code', '')
        admin = Users.get(Users.phone == phone)
        if admin:
            content = """<html>
                            <script>
                            alert("该用户已注册");
                            window.location.href='http://{0}/change_pwd';
                            </script>
                            </html>
                        """.format(request.host)
            return response.html(content)
        else:
            #默认注册账号为1级代理
            users = Users()
            users.username=name
            users.phone=phone
            users.password=pwd
            users.level=1
            users.user_code = uuid.uuid4()
            if code == "":
                users.agent_id=0
            else:
                invite_user = users.get(user_code=code)
                users.agent_id = invite_user.id
            users.save()
            balance = Balance()
            balance.username = name
            balance.phone = phone
            balance.amount = 0
            balance.commission = 0
            user = Users().get(Users.phone == phone)
            balance.user_id = user.id
            balance.save()
            content = """
                <html>
                <script>
                alert("注册成功");
                window.location.href='http://{0}/login';
                </script>
                </html>
            """.format(request.host)
            return response.html(content)
    else:
        user_code = request.args.get("user_code", "")
        return jinja.render("admin/change_pwd.html", request, user_code=user_code, message="")
