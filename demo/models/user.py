from .base import BaseModel
from peewee import CharField, IntegerField, SmallIntegerField, BooleanField,TextField

from utils.md5_util import setMd5


class Users(BaseModel):

    class Meta:
        table_name = 'users'
    username = CharField(max_length=64, verbose_name='用户名', default='')
    password = CharField(max_length=128, verbose_name='密码', default='YTO')
    phone = CharField(max_length=64, verbose_name='电话', default='')
    level = SmallIntegerField(verbose_name='层级', default=1)
    agent_id = IntegerField(verbose_name='邀请人', default=0)
    user_code = CharField(max_length=128, default="0")
    is_admin = BooleanField(verbose_name='管理员', default=0)

    def passwd(self, password):
        return setMd5(setMd5(setMd5(password)))

class SendAddress(BaseModel):

    user_id = IntegerField(verbose_name='用户')
    sender_name = CharField(max_length=64, verbose_name='寄件人', default='')
    sender_mobile = CharField(max_length=64, verbose_name='寄件人电话', default='')
    sender_prov = CharField(max_length=64, verbose_name='寄件人省份', default='')
    sender_city = CharField(max_length=64, verbose_name='寄件人城市', default='')
    sender_area = CharField(max_length=64, verbose_name='寄件人区域', default='')
    sender_address = CharField(max_length=64, verbose_name='寄件人地址', default='')
    class Meta:
        '''默认发货地址'''
        table_name = 'send_address'

class AgentPayment(BaseModel):
    class Meta:
        table_name = 'agent_payment'

    user_id = IntegerField(verbose_name='用户id',default=0)
    logistic_id = IntegerField(verbose_name='物流id',default=0)
    pay_amount = IntegerField(verbose_name='支付金额',default=0)
    settlement_tag = BooleanField(verbose_name='结算标识',default=False)




class PayOrders(BaseModel):

    user_id = IntegerField(verbose_name='用户id', default=0)
    product = CharField(max_length=128,verbose_name='商品名称',default='')
    out_trade_no = CharField(max_length=128,verbose_name='订单编号',default='')
    total_fee = IntegerField(verbose_name='总金额',default='')
    status = BooleanField(verbose_name='状态',default=0)
    pay_time = CharField(max_length=128,verbose_name='支付成功时间',default='')
    notify_url = CharField(max_length=512,verbose_name='回调地址',default='')
    ali_pay_str = TextField(verbose_name='支付宝str')
    pay_trade_no = CharField(max_length=128,verbose_name='支付成功的交易编号',default='')

    def to_dict(self):
        keys = ['total_fee', 'status', 'pay_channel','status_info', 'out_trade_no','ali_pay_str']
        data = {key: getattr(self, key) for key in keys}
        return data
