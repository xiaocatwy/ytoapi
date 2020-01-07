from .base import BaseModel
from peewee import CharField, IntegerField, SmallIntegerField, BooleanField ,FloatField


class Balance(BaseModel):
    class Meta:
        table_name = 'balance'

    user_id = IntegerField(verbose_name='用户id',default=0)
    username = CharField(max_length=64, verbose_name='用户名', default='')
    phone = CharField(max_length=64, verbose_name='电话', default='')
    amount = FloatField(verbose_name='余额',default=0)
    commission = FloatField(verbose_name="佣金",default=0)


# 佣金列表
class Commission(BaseModel):
    class Meta:
        table_name = 'commission'

    user_id = IntegerField(verbose_name='用户id', default=0)
    from_user_id = IntegerField(verbose_name='受邀人id', default=0)
    once_amount = FloatField(verbose_name='每一笔金额', default=0)
    detail = CharField(max_length=64, verbose_name='描述(受邀请人首冲｜受邀人下单)', default='')