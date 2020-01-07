#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: pay_order_handlers.py
@time: 2019/8/12 4:11 PM
@desc:
'''


import logging
import traceback
#支付宝初始化
from alipay import AliPay
from peewee import IntegerField, CharField, BooleanField

app_private_key_string = open("pay_key/private_2048.txt").read()
alipay_public_key_string = open("pay_key/alipay_public_key").read()


_alipay = AliPay(
    appid="2019060665470496",
    app_notify_url="https://alipay1.007vin.com/llqpay/alipay/notify",
    # app_private_key_path="pay_key/private_2048.txt",
    # alipay_public_key_path="pay_key/public_2048.txt"
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string
)


from models.user import PayOrders
@app.route("/order/pay",methods=['POST'])
async def create_orders(request):
    """微信网页支付请求发起"""
    try:
        product = request.form.get('product','')
        total_amount = request.form.get('total_amount','')
        pay_order = PayOrders()
        pay_order. user_id = IntegerField(verbose_name='用户id', default=0)
        product = CharField(max_length=128,verbose_name='商品名称',default='')
        out_trade_no = CharField(max_length=128,verbose_name='订单编号',default='')
        total_fee = IntegerField(verbose_name='总金额',default='')
        status = BooleanField(verbose_name='状态',default=0)
        pay_time = CharField(max_length=128,verbose_name='支付成功时间',default='')
        notify_url = CharField(max_length=512,verbose_name='回调地址',default='')
        ali_pay_str = CharField(max_length=512,verbose_name='支付宝str',default='')
        pay_trade_no = CharField(max_length=128,verbose_name='支付成功的交易编号',default='')

    except:
        logging.error(traceback.format_exc())

@app.route("/order/pay",methods=['POST'])
async def pay_jsapi(request):
    """微信网页支付请求发起"""
    try:
        product = request.form.get('product','')
        out_trade_no = request.form.get('out_trade_no','')
        pay_channel = request.form.get('pay_channel','weixin')
        total_amount = request.form.get('total_amount','')
        pay_from = request.form.get('pay_from', 'web')
        order_from = request.form.get('order_from','')
        notify_url = request.form.get('notify_url','')
        order_string = _alipay.api_alipay_trade_page_pay(out_trade_no=order.out_trade_no,
                                                                total_amount=order.total_fee/100,
                                                                subject=order.product,
                                                                return_url="https://alipay1.007vin.com/pay/alipay/notify")
    except:
        logging.error(traceback.format_exc())