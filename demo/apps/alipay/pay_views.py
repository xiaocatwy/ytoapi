#!/usr/bin/env python
# encoding: utf-8
'''
@author: tom_tao
@contact: tom_tao626@163.com
@file: pay_views.py
@time: 2019/8/27  下午6:30
@IDE: PyCharm
@desc: pay_views
'''

from services.pay_service import PayService
from apps import get_page_data
from base import jinja
from middleware.authorized import authorized
from models.user import PayOrders
from sanic import Blueprint

from conf import AGENT_COOKIE_TOKEN
from utils.cookie_util import get_cookies

pay_report_bp = Blueprint('pay_report')

@pay_report_bp.route("/pay_report/list",methods=['POST','GET'])
@authorized()
async def pay_report_info(request):
    if request.method == 'GET':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get("id")
        pay_report = PayOrders.select().filter(PayOrders.deleted == 0,PayOrders.user_id == user_id)
        kargs = {}
        kargs['user_id'] = request.args.get("user_id", "")
        kargs["out_trade_no"] = request.args.get("out_trade_no", "")
        # kargs["pay_trade_no"] = request.args.get("pay_trade_no","")
        query = PayService().query_pay_report(kargs,user_id)
        data = get_page_data(request, query)
        return jinja.render("admin/pay_report.html", request, data=data, kargs=kargs, pay_report=pay_report)