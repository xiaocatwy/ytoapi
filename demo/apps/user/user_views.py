#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: oeder_views.py
@time: 2019/6/22 9:32 PM
@desc:
'''

from playhouse.shortcuts import model_to_dict
from sanic.response import text, json_dumps, json

from middleware.authorized import authorized
from models.money import Balance
from services.user_service import UserService
from apps import get_page_data
from sanic import Blueprint, response
user_bp = Blueprint('user')
from models.user import Users
from conf import AGENT_COOKIE_TOKEN
from utils.cookie_util import get_cookies
from base import jinja

@user_bp.route("/user/list", methods=["GET", "POST"])
@authorized()
async def user_list(request):
    """
用户列表
:param request:
:return:
"""
    if request.method == 'GET':
        user_query = Users.select().filter(Users.deleted == 0)
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN,cookie)
        username = user.get('username')
        is_admin = user.get('is_admin')
        kargs = {}
        kargs['username'] = username
        kargs['is_admin'] = is_admin
        kargs['id'] = request.args.get("id","")
        kargs['phone'] = request.args.get("phone","")
        kargs["username"] = request.args.get("username", "")
        kargs["level"] = request.args.get("level", "")
        kargs["agent_id"] = request.args.get("agent_id", "")
        kargs["is_admin"] = request.args.get("is_admin", "")
        query = UserService().user_list(**kargs)
        data = get_page_data(request, query)
        return jinja.render("admin/user-list.html", request, kargs=kargs, data=data, user_query = user_query)
    elif request.method == "POST":
        id = request.form.get("id")
        Users.update({Users.deleted: 1}).where(Users.id == id).execute()
        return text("已删除")

@user_bp.route("/user/<show_id>", methods=["GET", "POST"])
@authorized()
async def user_update(request,show_id):
    '''
    信息修改
    :param request:
    :return:
    '''
    if request.method == 'GET':
        data = Users.select().filter(Users.show_id == show_id).get()
        data = model_to_dict(data)
        return jinja.render("admin/user-update.html", request, data = data)
    elif request.method == 'POST':
        data = request.form
        user_id = request.app.get_id_by_show_id(show_id)
        UserService().update_user(user_id, data)
        return text('修改完成')


#默认地址
from models.areas_do import Areas
@user_bp.route("/areas/get", methods=["GET", "POST"])
@authorized()
async def areas_handler(request):
    code = request.args.get('code','+86')
    areas = Areas.select().filter(Areas.parent_code==code).order_by(Areas.order.asc())
    data = [a.to_dict() for a in areas]
    return json(data)


@user_bp.route("/user/info", methods=["GET", "POST"])
@authorized()
async def agent_info(request):
    '''
    个人信息展示
    :param request:
    :return:
    '''
    if request.method == 'GET':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get("id")
        query = Users().select().filter(Users.deleted == 0,Users.id == user_id)
        code = Users().get(id=user_id)
        invite_url = "http://{}/change_pwd/?user_code={}".format(request.host,code.user_code)
        return jinja.render("admin/user_info.html", request, data=query,invite_url=invite_url)


@user_bp.route("/user/invite", methods=["GET", "POST"])
@authorized()
async def agent_info(request):
    if request.method == 'GET':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        kargs = {}
        kargs["agent_id"] = request.args.get("agent_id", "")
        kargs["username"] = request.args.get("username", "")
        kargs["user_id"] = request.args.get("user_id", "")
        query = UserService().query_invite(user,**kargs)
        data = get_page_data(request, query)
        return jinja.render("admin/invite_report.html", request, data=data, kargs=kargs)

# 佣金记录
@user_bp.route("/user/commission", methods=["GET", "POST"])
@authorized()
async def commission_info(request):
    if request.method == 'GET':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        kargs = {}
        kargs["user_id"] = request.args.get("user_id", "")
        kargs["from_user_id"] = request.args.get("from_user_id", "")
        query = UserService().query_commission(user,**kargs)
        data = get_page_data(request, query)
        return jinja.render("admin/commission_list.html", request, data=data, kargs=kargs)

# 佣金提现
@user_bp.route("/commission/cash", methods=["GET", "POST"])
@authorized()
async def commission_info(request):
    if request.method == 'POST':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        commission = request.form.get("commission")
        amount = request.form.get("amount")
        error = ""
        try:
            new_amount = float(amount) + float(commission)
            Balance().update({"commission": 0,"amount":new_amount}).where(Balance.user_id == user.get("id","")).execute()
        except Exception as e:
            error = str(e)
        if error:
            return json({'code': 0, 'info': '提现失败'})
        else:
            return json({'code': 1, 'info': '提现成功'})