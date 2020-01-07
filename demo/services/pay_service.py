#!/usr/bin/env python
# encoding: utf-8
'''
@author: tom_tao
@contact: tom_tao626@163.com
@file: pay_service.py
@time: 2019/8/27  下午6:21
@IDE: PyCharm
@desc: pay_service
'''

from models.user import PayOrders,Users
from .base_service import BaseService

class PayService(BaseService):
    def query_pay_report(self, kargs,user_id):
        user = Users.get(Users.id == user_id)
        query = PayOrders.select().filter(PayOrders.deleted == 0)
        if not user.is_admin:
            query =query.filter(PayOrders.user_id == user_id)
        if kargs.get("out_trade_no", ""):
            query = query.filter(PayOrders.out_trade_no.contains(kargs["out_trade_no"]))
        if kargs.get("pay_trade_no", ""):
            query = query.filter(PayOrders.pay_trade_no.contains(kargs["pay_trade_no"]))
        query = query.order_by(PayOrders.create_time.desc())
        return query