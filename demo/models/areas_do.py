#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: areas_do.py
@time: 2019/8/8 9:48 AM
@desc:
'''

from peewee import *
from models.base import db

class Areas(Model):

    code = CharField(max_length=16, verbose_name="城市码")
    name = CharField(max_length=32, verbose_name='名称')
    parent_code = CharField(max_length=16, verbose_name='父码', default='')
    order = IntegerField(verbose_name='顺序')

    class Meta:
        table_name = 'areas'
        database = db
        verbose_name = '地址'

    def to_dict(self):
        keys = ['code', 'name']
        data = {key: getattr(self, key) for key in keys}
        return data

    @classmethod
    def get_area_by_code(cls,code):
        obj = cls.get(cls.code==code)
        return obj