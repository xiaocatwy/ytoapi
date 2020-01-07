#!/usr/bin/env python
# encoding: utf-8
'''
@author: tom_tao
@contact: tom_tao626@163.com
@file: area_view.py
@time: 2019/8/21  上午11:31
@IDE: PyCharm
@desc: area_view
'''
import time

from sanic import Blueprint, response
from sanic.response import text
from services.area_service import AreaService

from base import jinja
from apps import get_page_data

from models.areas_do import Areas

from conf import AGENT_COOKIE_TOKEN
from utils.cookie_util import get_cookies

position_bp = Blueprint('position')
from models.user import SendAddress
from middleware.authorized import authorized

@position_bp.route("/position/list", methods=["GET", "POST"])
@authorized()
async def area_list(request):
    '''
    地址管理
    :param request:
    :return:
    '''
    if request.method == 'GET':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get("id")
        send = SendAddress.select().filter(SendAddress.user_id==user_id,SendAddress.deleted == 0)
        areas = Areas.select().filter(Areas.parent_code == '+86').order_by(Areas.order.asc())
        kargs = {}
        kargs["sender_name"] = request.args.get("sender_name", "")
        kargs["sender_mobile"] = request.args.get("sender_mobile", "")
        query = AreaService().query_list(user_id,**kargs)
        data = get_page_data(request, query)
        return jinja.render("admin/area_list.html", request, kargs=kargs, data=data, areas=areas,send=send)
    elif request.method == "POST":
        id = request.form.get("id")
        SendAddress.update({SendAddress.deleted: 1}).where(SendAddress.id == id).execute()
        return text("已删除")


@position_bp.route("/position/add", methods=['GET', 'POST'])
@authorized()
async def area_add(request):
    '''
    添加地址
    :param request:
    :return:
    '''
    if request.method == 'GET':
        send = SendAddress.select().filter(SendAddress.deleted == 0)
        areas = Areas.select().filter(Areas.parent_code == '+86').order_by(Areas.order.asc())
        return jinja.render("admin/area_add.html", request, areas=areas, send=send)
    elif request.method == "POST":
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get("id")
        data = request.form
        if request.form.get("sender_prov", ""):
            data["sender_prov"] = Areas.get(Areas.code==request.form.get("sender_prov", "")).name
        else:
            data["sender_prov"] = request.form.get("sender_prov", "")
        if request.form.get("sender_city", ""):
            data["sender_city"] = Areas.get(Areas.code == request.form.get("sender_city", "")).name
        else:
            data["sender_city"] = request.form.get("sender_city", "")
        if request.form.get("sender_area", ""):
            data["sender_area"] = Areas.get(Areas.code == request.form.get("sender_area", "")).name
        else:
            data["sender_area"] = request.form.get("sender_area", "")
        AreaService().add_Area(data, user_id)
        return text("添加完成")


@position_bp.route("/position/update/<show_id>", methods=['GET', 'POST'])
@position_bp.route("/position/update", methods=['GET', 'POST'])
@authorized()
async def area_update(request,show_id=''):
    '''
    更新地址
    :param request:
    :param show_id:
    :return:
    '''
    if request.method == 'GET':
        show_id = request.args.get("show_id")
        areas = Areas.select().filter(Areas.parent_code == '+86').order_by(Areas.order.asc())
        send = SendAddress.get(SendAddress.id == request.app.get_id_by_show_id(show_id))
        return jinja.render("admin/area_update.html", request, send=send, areas=areas)
    if request.method == 'POST':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        data = request.form
        kargs = {key: value[0] for key, value in data.items()}

        {'sender_name': '赵六', 'sender_mobile': '1221212121',
         'sender_prov': '14', 'sender_city': '杭州市', 'sender_area': '余杭区',
         'sender_address': '231312312'}
        try:
            prov_code = int(kargs.pop('sender_prov'))
            sender_prov = Areas.get(Areas.code==prov_code).name
            city_code = int(kargs.pop('sender_city'))
            sender_city = Areas.get(Areas.code == city_code).name
            area_code = int(kargs.pop('sender_area'))
            sender_area = Areas.get(Areas.code == area_code).name
        except:
            pass
        kargs.update({'sender_prov':sender_prov,'sender_city':sender_city,'sender_area':sender_area})
        SendAddress.update(**kargs).where(SendAddress.id == request.app.get_id_by_show_id(show_id),
                                        SendAddress.user_id == request.app.get_id_by_show_id(user.get('show_id'))).execute()
        return text('修改成功')