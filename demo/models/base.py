#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: base.py
@time: 2019/1/18 11:58 AM
@desc:
'''
from peewee import OperationalError,DateTimeField, MySQLDatabase,SqliteDatabase,BooleanField,CharField
import datetime
from playhouse.signals import Model, post_save
from peewee import __exception_wrapper__

from conf.mysql_conf import db_conf
import random
user = db_conf

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

class RetryMySQLDatabase(RetryOperationalError, MySQLDatabase):
    pass

db = RetryMySQLDatabase(database=user.get('db_conn'),
                       user=user.get('username'),
                       password=user.get('pwd'),
                       host=user.get('host'),
                       port=user.get('port'))
# db  = SqliteDatabase('wei.db_conn')
# print(db_conn)

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


@post_save(sender=BaseModel)
def on_save_handler(model_class, instance, created):
    '''
    自动填充show_id
    :param model_class:
    :param instance:
    :param created:
    :return:
    '''
    if not instance.show_id:
        if hasattr(instance,'sn_no'):
            sn_no = instance.set_show_id_by_id(instance.id)+str(instance.id)
            model_class.update({model_class.show_id:instance.set_show_id_by_id(instance.id),model_class.sn_no:sn_no}).where(model_class.id==instance.id).execute()
        else:
            model_class.update({model_class.show_id:instance.set_show_id_by_id(instance.id)}).where(model_class.id==instance.id).execute()
    else:
        model_class.update({model_class.update_time:datetime.datetime.now()}).where(model_class.id==instance.id).execute()


#python -m pwiz -e mysql -H localhost -p 3306 -u root -P  -t table_names database_name > model.py
#python -m pwiz -e mysql -H 192.168.191.14 -p 3306 -u users -P  -t users users > users.py
#python -m pwiz -e mysql -H 192.168.191.14 -p 3306 -u users -P  -t  ugc_parts_label users > ugc_parts_label_do.py
#python -m pwiz -e mysql -H 192.168.191.14 -p 3306 -u users -P  -t  ugc_parts_price users > ugc_parts_price_do.py
#python -m pwiz -e mysql -H 192.168.191.14 -p 3306 -u users -P  -t  ugc_parts_detail_history users > ugc_parts_detail_history.py
#python -m pwiz -e mysql -H 192.168.191.14 -p 3306 -u users -P  -t  user_inventory_wanted users > user_inventory_wanted.py

#id  show_id