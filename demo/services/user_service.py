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
from models.user import Users
from models.money import Commission

class UserService(BaseService):

    def user_list(self,**kargs):
        '''
        查询生产批次列表
        :param kargs:
        :return:
        '''
        query = Users.select().filter(Users.deleted==0)
        if "id" in kargs and kargs.get('id').strip():
            query = query.filter(id=int(kargs["id"]))
        if "username" in kargs and kargs.get('username').strip():
            query = query.filter(username=kargs["username"])
        if "level" in kargs and kargs.get('level').strip():
            query = query.filter(level=kargs["level"])
        if "agent_id" in kargs and kargs.get('agent_id').strip():
            query = query.filter(agent_id=kargs["agent_id"])
        if "is_admin" in kargs and kargs.get('is_admin').strip():
            query = query.filter(is_admin=kargs["is_admin"])
        if "phone" in kargs and kargs.get("phone").strip():
            query = query.filter(phone=kargs["phone"])
        return query

    def update_user(self, user_id, data):
        '''
        修改
        :param show_id:
        :param data:
        :return:
        '''
        user = Users.get(Users.id == user_id)
        if "username" in data and data.get("username").strip():
            user.username = data.get("username")
        if "phone" in data and data.get("phone").strip():
            user.phone = data.get("phone")
        if "password" in data and data.get("password").strip():
            user.password = Users().passwd(data.get('password'))
        if "level" in data and data.get("level").strip():
            user.level = data.get("level")
        user.save()

    def query_invite(self,user,**kargs):
        if user.get("is_admin","")==True:
            query = Users.select().filter(Users.deleted==0,Users.agent_id==kargs.get("agent_id","")).order_by(Users.create_time.desc())
        else:
            query = Users.select().filter(Users.deleted==0,Users.agent_id==user.get("id")).order_by(Users.create_time.desc())
        if "username" in kargs and kargs.get('username').strip():
            query = query.filter(username=kargs["username"])
        if "user_id" in kargs and kargs.get('user_id').strip():
            query = query.filter(id=kargs["user_id"])
        return query

    def query_commission(self, user, **kargs):
        if user.get("is_admin", "") == True:
            query = Commission.select().filter(Commission.deleted == 0, Commission.user_id == kargs.get("user_id", ""))
        else:
            query = Commission.select().filter(Commission.deleted == 0, Commission.user_id == user.get("id")).order_by(Commission.create_time.desc())
        # if "username" in kargs and kargs.get('username').strip():
        #     query = query.filter(username=kargs["username"])
        if "from_user_id" in kargs and kargs.get('from_user_id').strip():
            query = query.filter(from_user_id=kargs["from_user_id"])
        return query
