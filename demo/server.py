#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 下午11:15
# @Author  : qiuyan
# @Site    : 
# @File    : server.py
# @Software: PyCharm

from base import app
from sanic.log import logger as log
from base import jinja
from sanic.response import text
from sanic import response
from sanic.exceptions import ServerError

import os
from sanic.log import error_logger
# ----------------------------------------------- #
# load apps
# ----------------------------------------------- #

from apps.alipay.pay_views import pay_report_bp
app.blueprint(pay_report_bp)

from apps.areas_handlers import area_bp
app.blueprint(area_bp)

from apps.area.area_views import position_bp
app.blueprint(position_bp)

from apps.login.login_way import login_bp
app.blueprint(login_bp)

from apps.order.oeder_views import order_bp
app.blueprint(order_bp)

from apps.user.user_views import user_bp
app.blueprint(user_bp)

from apps.balance.balance_view import balance_bp
app.blueprint(balance_bp)

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
import xmltodict
import requests
import urllib
import time
import xlrd
import random
import os
from sanic.response import file




# 后台登录验证
from middleware.authorized import authorized
@app.route("/")
@authorized()
async def index(request):
    user = request.app.user
    return jinja.render('admin/index.html', request, users=user)



#加载静态文件
from sanic import Blueprint
static_bp = Blueprint('bp')
static_bp.static('/static', './static')
static_bp.static('/favicon.ico', './static/favicon.ico')
static_bp.static('/js', './static/js')
static_bp.static('/css', './static/css')
static_bp.static('/lib', './static/lib')
# static_bp.static('/upload', './upload')
# static_bp.static('/assets/fonts', './static/assets/fonts')
# static_bp.static('/assets/img', './static/assets/img')
# static_bp.static('/assets/js', './static/assets/js')
# static_bp.static('/assets/css', './static/assets/css')
app.blueprint(static_bp)



@app.exception(ServerError)
async def test(request, exception):
    return response.json({"exception": "{}".format(exception), "status": exception.status_code},
                         status=exception.status_code)


from models.base import db

@app.middleware('response')
async def after_response(request, response):
    try:
        if not db.is_closed():
            db.close()
    except:
        error_logger.error()

from base import set_show_id_by_id,get_id_by_show_id
@app.listener('before_server_start')
def before_start(app, loop):
    app.set_show_id_by_id = set_show_id_by_id
    app.get_id_by_show_id = get_id_by_show_id
    log.info("SERVER STARTING")


import sys
if __name__ == '__main__':

    try:
        port = int(sys.argv[1])
    except:
        port = 8001

    app.run(host="0.0.0.0", port=port, debug=True)