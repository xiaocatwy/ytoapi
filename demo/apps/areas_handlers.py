#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: areas_handlers.py
@time: 2019/8/8 10:20 AM
@desc:
'''

from sanic import Blueprint, response
from sanic.response import json
from models.areas_do import Areas
area_bp = Blueprint('area')

@area_bp.route("/area/get", methods=["GET", "POST"])
async def areas_handler(request):
    code = request.args.get('code','+86')
    areas = Areas.select().filter(Areas.parent_code==code).order_by(Areas.order.asc())
    data = [a.to_dict() for a in areas]
    return json(data)


