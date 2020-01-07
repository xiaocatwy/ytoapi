#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: produce_service.py
@time: 2019/6/22 10:06 PM
@desc:
'''
from .base_service import BaseService
from models.order import UserLogistic

class OrderService(BaseService):

    def query_list(self,users,**kargs):
        '''
        查询列表
        :param kargs:
        :return:
        '''
        if users.get("is_admin","")==True:
            query = UserLogistic.select().filter(UserLogistic.deleted == 0).order_by(UserLogistic.create_time.desc())
            if "mailNo" in kargs and kargs.get('mailNo').strip():
                query = query.filter(mailNo=kargs["mailNo"])
            if "sender_name" in kargs and kargs.get('sender_name').strip():
                query = query.filter(sender_name=kargs["sender_name"])
            if "sender_mobile" in kargs and kargs.get('sender_mobile').strip():
                query = query.filter(sender_mobile=kargs["sender_mobile"])
            if "recive_name" in kargs and kargs.get('recive_name').strip():
                query = query.filter(recive_name=kargs["recive_name"])
            if "recive_mobile" in kargs and kargs.get('recive_mobile').strip():
                query = query.filter(recive_mobile=kargs["recive_mobile"])

        else:
            query = UserLogistic.select().filter(UserLogistic.deleted==0,UserLogistic.user_id==int(users.get("id", "0")))
            if "user_id" in kargs and kargs.get('user_id').strip():
                query = query.filter(user_id=kargs["user_id"])
            if "mailNo" in kargs and kargs.get('mailNo').strip():
                query = query.filter(mailNo=kargs["mailNo"])
            if "sender_name" in kargs and kargs.get('sender_name').strip():
                query = query.filter(sender_name=kargs["sender_name"])
            if "sender_mobile" in kargs and kargs.get('sender_mobile').strip():
                query = query.filter(sender_mobile=kargs["sender_mobile"])
            if "recive_name" in kargs and kargs.get('recive_name').strip():
                query = query.filter(recive_name=kargs["recive_name"])
            if "recive_mobile" in kargs and kargs.get('recive_mobile').strip():
                query = query.filter(recive_mobile=kargs["recive_mobile"])
        query = query.order_by(UserLogistic.create_time.desc())
        return query
