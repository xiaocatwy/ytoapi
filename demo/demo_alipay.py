#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: demo_alipay.py
@time: 2019/8/26 6:04 PM
@desc:
'''

#支付宝初始化
from alipay import AliPay
app_private_key_string = open("alipay/private_key_2048.txt").read()
alipay_public_key_string = open("alipay/alipay_pub_key").read()

_alipay = AliPay(
    appid="2019082666427588",
    app_notify_url="http://api.ytodanhao.com.cn/alipay/notify",
    # app_private_key_path="pay_key/private_2048.txt",
    # alipay_public_key_path="pay_key/public_2048.txt"
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string
)


order_string = _alipay.api_alipay_trade_app_pay(out_trade_no='2019082618092',
                                                                total_amount=100,
                                                                subject='厨房电器勺子')
print(order_string)