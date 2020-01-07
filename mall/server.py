#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 下午11:15
# @Author  : qiuyan
# @Site    : 
# @File    : server.py
# @Software: PyCharm

import random
from sanic import Sanic
from sanic.response import html
app = Sanic(__name__)
from sanic.log import logger

from jinja2 import Environment, PackageLoader
import os
jinjaEnv = Environment(loader=PackageLoader('__main__', 'ui'))


@app.route("/")
async def index(request):
    template = jinjaEnv.get_template('home.htm')
    html_content = template.render()
    return html(html_content)


@app.route("/order")
async def index(request):
    order_id = request.args.get('order_id')
    template = jinjaEnv.get_template('order.htm')
    html_content = template.render(order_id=order_id)
    return html(html_content)

#加载静态文件
from sanic import Blueprint
static_bp = Blueprint('bp')
static_bp.static('/static', './static')
app.blueprint(static_bp)

import sys
if __name__ == '__main__':

    try:
        port = int(sys.argv[1])
    except:
        port = 8001

    app.run(host="0.0.0.0", port=port, debug=True)