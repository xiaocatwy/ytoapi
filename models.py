#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: models.py
@time: 2019/7/26 2:29 PM
@desc:
'''
from peewee import OperationalError, DateTimeField, MySQLDatabase,SmallIntegerField, SqliteDatabase, BooleanField, CharField,TextField,IntegerField
import datetime
from playhouse.signals import Model, post_save
from peewee import __exception_wrapper__
import random

class RetryOperationalError(object):
    def execute_sql(self, sql, params=None, commit=True):
        try:
            cursor = super(RetryOperationalError, self).execute_sql(
                sql, params, commit)
        except OperationalError:
            if not self.is_closed():
                self.close()
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        return cursor


class RetrySqliteDatabase(RetryOperationalError, SqliteDatabase):
    pass

db = RetrySqliteDatabase('yto.db')


class BaseModel(Model):
    class Meta:
        database = db

    show_id = CharField(max_length=128,verbose_name='展示ID',default='')
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now, index=True)
    deleted = BooleanField(verbose_name='删除',default=False)

    def get_id_by_show_id(self, showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
        i = showId[len(showId) - 1]
        j = showId[0:len(showId) - 1]
        k = (int(j) - int(i) - 10000) / int(i)
        return k

    def set_show_id_by_id(self, id):
        '''
        设置showid
        :param id: 真实id
        :return:
        '''
        a = random.randint(1, 9)
        b = a * int(id) + 10000 + a
        j = str(b) + str(a)
        return j

    def to_dict(self,keys):
        data={}
        for key in keys:
            value = getattr(self,key)
            if isinstance(value,datetime.datetime):
                data[key]=value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[key] = value
        #data = {key:getattr(self,key) for key in keys}
        return data

    @classmethod
    def get(cls, *query, **filters):
        try:
            sq = cls.select()
            if query:
                sq = sq.where(*query)
            if filters:
                sq = sq.filter(**filters)
            return sq.get()
        except:
            return None

class Users(BaseModel):

    class Meta:
        table_name = 'users'

    username = CharField(max_length=64, verbose_name='用户名', default='')
    password = CharField(max_length=64, verbose_name='密码', default='YTO')
    phone = CharField(max_length=64, verbose_name='电话', default='')
    level = SmallIntegerField(verbose_name='层级', default=1)
    agent_id = IntegerField(verbose_name='邀请人',default=0)
    is_admin = BooleanField(verbose_name='管理员',default=0)

class AgentPayment(BaseModel):
    class Meta:
        table_name = 'agent_payment'

    user_id = IntegerField(verbose_name='用户id',default=0)
    logistic_id = IntegerField(verbose_name='物流id',default=0)
    pay_amount = IntegerField(verbose_name='支付金额',default=0)
    settlement_tag = BooleanField(verbose_name='结算标识',default=False)


class UserLogistic(BaseModel):
    class Meta:
        table_name = 'user_logistic'

    user_id = IntegerField(verbose_name='用户ID',default=0)
    mailNo = CharField(max_length=64, verbose_name='物流单号', default='')
    clientID = CharField(max_length=64, verbose_name='ClientID', default='')
    logisticProviderID = CharField(max_length=64, verbose_name='logisticProviderID', default='YTO')
    customerId = CharField(max_length=64, verbose_name='customerId', default='')
    txLogisticID = CharField(max_length=64, verbose_name='customerId', default='')
    tradeNo = CharField(max_length=64, verbose_name='customerId', default='')
    orderType = CharField(max_length=64, verbose_name='customerId', default='1')
    serviceType = CharField(max_length=64, verbose_name='customerId', default='0')
    itemsWeight = CharField(max_length=64, verbose_name='customerId', default='0.0')
    flag = CharField(max_length=64, verbose_name='customerId', default='0')
    goodsValue = CharField(max_length=64, verbose_name='customerId', default='0')
    special = CharField(max_length=64, verbose_name='customerId', default='0')
    insuranceValue = CharField(max_length=64, verbose_name='customerId', default='0.0')
    totalServiceFee = CharField(max_length=64, verbose_name='customerId', default='0.0')
    codSplitFee = CharField(max_length=64, verbose_name='customerId', default='0.0')

    sender_name = CharField(max_length=64, verbose_name='寄件人', default='')
    sender_mobile = CharField(max_length=64, verbose_name='寄件人电话', default='')
    sender_prov = CharField(max_length=64, verbose_name='寄件人省份', default='')
    sender_city = CharField(max_length=64, verbose_name='寄件人城市', default='')
    sender_address = CharField(max_length=64, verbose_name='寄件人地址', default='')

    recive_name = CharField(max_length=64, verbose_name='收货人', default='')
    recive_mobile = CharField(max_length=64, verbose_name='收货人电话', default='')
    recive_prov = CharField(max_length=64, verbose_name='收货人省份', default='')
    recive_city = CharField(max_length=64, verbose_name='收货人城市', default='')
    recive_address = CharField(max_length=64, verbose_name='收货人地址', default='')
    items = TextField(verbose_name='物品信息,json格式')

    settlement_tag = BooleanField(verbose_name='结算标识',default=False)

    def get_id_by_show_id(self, showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
        i = showId[len(showId) - 1]
        j = showId[0:len(showId) - 1]
        k = (int(j) - int(i) - 10000) / int(i)
        return k

    def set_show_id_by_id(self, id):
        '''
        设置showid
        :param id: 真实id
        :return:
        '''
        a = random.randint(1, 9)
        b = a * int(id) + 10000 + a
        j = str(b) + str(a)
        return j

    def to_dict(self, keys):
        data = {}
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, datetime.datetime):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[key] = value
        # data = {key:getattr(self,key) for key in keys}
        return data

    @classmethod
    def get(cls, *query, **filters):
        try:
            sq = cls.select()
            if query:
                sq = sq.where(*query)
            if filters:
                sq = sq.filter(**filters)
            return sq.get()
        except:
            return None
