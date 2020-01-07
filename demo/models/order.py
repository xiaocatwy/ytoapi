#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: device_do.py
@time: 2019/6/20 11:03 AM
@desc:
'''
from peewee import *
from models.base import BaseModel


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
    weight = CharField(max_length=32, verbose_name='customerId', default='0')
    price = FloatField(verbose_name='customerId', default='')
    settlement_tag = BooleanField(verbose_name='结算标识',default=False)
