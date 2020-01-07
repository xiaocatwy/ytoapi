#!/usr/bin/env python
# encoding: utf-8
'''
@author: tom_tao
@contact: tom_tao626@163.com
@file: area_service.py
@time: 2019/8/20  下午6:19
@IDE: PyCharm
@desc: area_service
'''

from playhouse.shortcuts import model_to_dict

from .base_service import BaseService
from models.user import SendAddress

class AreaService(BaseService):


    def query_list(self, user_id, **kargs):
        '''
        显示默认地址列表
        :param kargs:
        :return:
        '''
        query = SendAddress.select().filter(SendAddress.user_id==user_id,SendAddress.deleted == 0)
        if kargs["sender_name"]:
            query = query.filter(sender_name=kargs["sender_name"])
        if kargs["sender_mobile"]:
            query = query.filter(sender_mobile=kargs["sender_mobile"])
        return query

    def add_Area(self,data,user_id):
        '''
        添加默认地址
        :param kargs:
        :return:
        '''
        area = SendAddress()
        area.user_id = user_id
        area.sender_name = data.get("sender_name")
        area.sender_mobile = data.get("sender_mobile")
        area.sender_prov = data['sender_prov']
        area.sender_city = data["sender_city"]
        area.sender_area =  data["sender_area"]
        area.sender_address = data.get("sender_address")
        area.save()

    def update_Area(self, show_id, **kargs):
        '''
        修改默认地址
        :param show_id:
        :param kargs:
        :return:
        '''
        info = SendAddress.update(**kargs).where(SendAddress.id == show_id).execute()
        return info