#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: base_service.py
@time: 2019/6/22 10:07 PM
@desc:
'''

import ujson
import re
# from blinker import signal
import timeit
import traceback
import logging
import random

class BaseService(object):

    def __init__(self):
        pass
    def get_id_by_show_id(self, showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
        if isinstance(showId, int):
            showId = str(showId)
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
