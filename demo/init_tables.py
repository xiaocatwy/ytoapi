#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: init_tables.py
@time: 2019/2/15 10:14 AM
@desc:
'''

from models.base import db
import logging
import random
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from models.user import Users, AgentPayment,SendAddress,PayOrders
from models.order import UserLogistic
from models.money import Balance,Commission
from models.areas_do import Areas
import datetime
db.connect()

tables=[Users, AgentPayment, UserLogistic, SendAddress, PayOrders, Areas, Balance,Commission]

def init_tables():
    db.drop_tables(tables)
    db.create_tables(tables)

def init_user():
    user = Users()
    user.username="boss"
    user.phone="17830466355"
    user.is_admin=1
    user.level=1
    user.password=user.passwd("466355")
    user.save()

def init_area():
    f = open('areas.sql', 'r')
    sql = f.readline()
    while sql:
        db.execute_sql(sql)
        sql = f.readline()
    f.close()

def init_balance():
    balance = Balance()
    balance.username="boss"
    balance.phone="17830466355"
    balance.amount=0
    balance.commission=0
    user = Users().get(Users.phone=="17830466355")
    balance.user_id=user.id
    balance.save()

import time
time.sleep(1)
init_tables()
print ('--------------初始化表--------------------')
time.sleep(1)
init_user()
print ('--------------初始--------------------')
time.sleep(1)
init_area()
print ('--------------初始区域信息--------------------')
init_balance()
time.sleep(1)
db.commit()