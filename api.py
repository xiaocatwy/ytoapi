#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: api.py
@time: 2019/7/24 4:32 PM
@desc:
'''

import time
from sanic import response
from sanic import request
from sanic.request import json_loads
import xmltodict
import random
from sanic.response import json_dumps,text,json
from sanic import Sanic
from sanic_jinja2 import SanicJinja2

app = Sanic(__name__)
jinja = SanicJinja2(app,loader=None,pkg_name='',pkg_path='')

from sanic import Blueprint

#
# 客户码：  （拉单）秘钥：    管理账号：K12478670  （初始）密码：Uy0La9NE(!qazxsW2)  （重量）秘钥：
# K11122126  重量秘钥  7d35f6f98e025b85b75c283260af5d09

config = {
	"YTO":"YTO",
	"UrlOrder":"http://service.yto56.net.cn/CommonOrderModeBPlusServlet.action",
	"UrlWeight":"http://116.228.115.225:6183/3rdface/open-service/persist/weight",
	"ClientID":"K11122126",
	"ClientSec":"D570nY8Y",
	"WeightSec":"7d35f6f98e025b85b75c283260af5d09"
}

# api_bp = Blueprint('api')


import hashlib
import base64

def signatral(xml_body, client_sec):
    '''
    签名
    :param xml_body:
    :param client_sec:
    :return:
    '''
    m = hashlib.md5()
    data= xml_body+client_sec
    if isinstance(xml_body,bytes):
        m.update(data.encode('utf-8'))
    else:
        m.update(data.encode('utf-8'))
    str_result = base64.b64encode(m.digest())
    return str_result

sender = {"name":"", "mobile":"", "prov":"","city":"", "address":""}
recive = {"name":"", "mobile":"", "prov":"", "city":"", "address":""}
item = {"itemName":"", "number":"", "itemValue":""}

custom_root = 'RequestOrder'
from dicttoxml import dicttoxml
import xmltodict
import requests
import urllib
import time

@app.route('/')
async def home(request):
    return jinja.render('form.html',request)

@app.route('/common/order/model',methods=['POST'])
async def command_order(request):

    print(request.form)
    keys=['sender_name','sender_mobile','sender_prov','sender_city','sender_address',
          'recive_name','recive_mobile','recive_prov','recive_city','recive_address',
          'itemName','number'
          ]
    for key in keys:
        if not request.form.get(key,'').strip():
            return json({'code':0,'msg':'参数{0}'.format(key)+'不能为空'})
        if len(request.form.get(key))>256:
            return json({'code': 0, 'msg': '参数{0}'.format(key) + '长度不能超过256'})
    params = request.form
    sender.update({"name":params.get('sender_name'), "mobile":params.get('sender_mobile'), "prov":params.get('sender_prov'),"city":params.get('sender_city'), "address":params.get('sender_address')})
    recive.update({"name":params.get('recive_name'), "mobile":params.get('recive_mobile'), "prov":params.get('recive_prov'),"city":params.get('recive_city'), "address":params.get('recive_address')})

    items=[]
    itemNames = request.form.get('itemName')
    numbers = request.form.get('number')
    itemValues = request.form.get('itemValue')
    weight = request.form.get('weight')

    # if isinstance(itemNames,list) and isinstance(numbers,list):
    #     item_list = zip(itemNames,numbers,itemValues)
    #     for name,num,value in item_list:
    #         if name and num:
    #             items.append({"itemName":name, "number":num, "itemValue":value})
    # else:

    items.append({"itemName": itemNames, "number": numbers, "itemValue": itemValues})

    order_id = str(int(time.time() * 1000000))+str(random.randint(10,1000))

    data={'clientID':config.get('ClientID'),'logisticProviderID':'YTO',
               'customerId':config.get('ClientID'),'txLogisticID':order_id,
               'tradeNo':'','orderType':1,'serviceType':0,
               'itemsWeight':0.0,'flag':0,'goodsValue':0,'special':0,
               'insuranceValue':0.0,'totalServiceFee':0.0,'codSplitFee':0.0}
    data.update({"sender":sender,"receiver":recive,'items':items})
    xml_body=dicttoxml(data,root=True,custom_root=custom_root,attr_type=False)
    xml_body = xml_body.decode().replace('<?xml version="1.0" encoding="UTF-8" ?>','')
    #xml_body='<RequestOrder><clientID>K11122126</clientID><logisticProviderID>YTO</logisticProviderID><customerId>K11122126</customerId><txLogisticID>K11122126abc1004</txLogisticID><tradeNo>K11122126</tradeNo><orderType>1</orderType><serviceType>0</serviceType><itemsWeight>1.2</itemsWeight><flag>0</flag><goodsValue>0</goodsValue><special>0</special><insuranceValue>0.0</insuranceValue><totalServiceFee>0.0</totalServiceFee><codSplitFee>0.0</codSplitFee><sender><name>张三</name><mobile>13550031574</mobile><prov>浙江省</prov><city>杭州市</city><address>滨江区网商路599号</address></sender><receiver><name>李四</name><mobile>13550031578</mobile><prov>四川省</prov><city>成都市</city><address>龙泉驿区西河镇</address></receiver><items><item><itemName>男式衣服</itemName><number>1</number><itemValue>25</itemValue></item></items></RequestOrder>'
    data_digest = signatral(xml_body,config.get('ClientSec'))
    # print(data_digest)
    #data_digest='E9yeCCnxCFLmQs8bHM+oZQ=='
    params = {'clientId':config.get('ClientID'),'data_digest':data_digest,'logistics_interface':xml_body}
    #data = urllib.parse.urlencode(params)
    config.get('UrlOrder') + '?' + urllib.parse.urlencode(params)
    # print(urllib.parse.urlencode(params))
    res = requests.post(config.get('UrlOrder')+'?'+urllib.parse.urlencode(params))
    content = res.text
    res_data = xmltodict.parse(content)

    if res_data.get('Response').get('success') in ('true',True):
        address = res_data['Response'].pop('distributeInfo')
        res_data = dict(res_data['Response'].items())
        res_data.update({'distributeInfo':dict(address)})
        #存库
        if request.form.get('weight',''):
            paramSetWeight ={'waybillNo':order_id,'weight':weight,'customerCode':config.get('ClientID'),'clientId':config.get('WeightSec')}
            req = requests.get(config.get('UrlWeight'),params=paramSetWeight)
            w_text = req.text
            print(w_text)
        return json({'code':1,'data':res_data})
    else:
        data = dict(res_data['Response'].items())
        return json({'code':0,'data':data})

import time
import xlrd
import os
from sanic.response import file
@app.route('/download/excel')
async def excel_download(request):
    return await response.file_stream("圆通单号模板.xls",filename="圆通单号模板.xls")


@app.route('/yto/upload',methods=['POST'])
async def excel_upload(request):
    img_file = request.files.get('ytofile')
    if img_file:
        file_parameters = {
            'body': img_file.body,
            'name': img_file.name,
            'type': img_file.type,
        }
        filename = img_file.name
        f = open(filename,'wb')
        f.write(img_file.body)
        f.close()
        # 只能读不能写
        book = xlrd.open_workbook(filename)  # 打开一个excel
        sheet = book.sheet_by_index(0)  # 根据顺序获取sheet
        fail=[]
        for i in range(sheet.nrows):  # 0 1 2 3 4 5
            if i==0:
                continue
            row_values = sheet.row_values(i)
            sender={"name": row_values[0], "mobile": row_values[1],"prov": row_values[2], "city": row_values[3],"address":row_values[4]}
            recive = {"name": row_values[5], "mobile":row_values[6],"prov": row_values[7], "city":row_values[8],"address":row_values[9]}
            items = [{"itemName": row_values[10], "number": int(row_values[11]), "itemValue": row_values[12]}]
            weight = row_values[13]
            order_id = str(int(time.time() * 1000000)) + str(random.randint(10, 1000))
            data = {'clientID': config.get('ClientID'), 'logisticProviderID': 'YTO',
                    'customerId': config.get('ClientID'), 'txLogisticID': order_id,
                    'tradeNo': '', 'orderType': 1, 'serviceType': 0,
                    'itemsWeight': 0.0, 'flag': 0, 'goodsValue': 0, 'special': 0,
                    'insuranceValue': 0.0, 'totalServiceFee': 0.0, 'codSplitFee': 0.0}
            data.update({"sender": sender, "receiver": recive, 'items': items})
            xml_body = dicttoxml(data, root=True, custom_root=custom_root, attr_type=False)
            xml_body = xml_body.decode().replace('<?xml version="1.0" encoding="UTF-8" ?>', '')
            data_digest = signatral(xml_body, config.get('ClientSec'))
            params = {'clientId': config.get('ClientID'), 'data_digest': data_digest, 'logistics_interface': xml_body}
            config.get('UrlOrder') + '?' + urllib.parse.urlencode(params)
            res = requests.post(config.get('UrlOrder') + '?' + urllib.parse.urlencode(params))
            content = res.text
            res_data = xmltodict.parse(content)


            if res_data.get('Response').get('success') in ('true', True):
                address = res_data['Response'].pop('distributeInfo')
                data = dict(res_data['Response'].items())
                data.update({'distributeInfo': dict(address)})
                #存库
                if request.form.get('weight', ''):
                    paramSetWeight = {'waybillNo': order_id, 'weight':weight, 'customerCode': config.get('ClientID'),
                                      'clientId': config.get('WeightSec')}
                    req = requests.get(config.get('UrlWeight'), params=paramSetWeight)
                    w_text = req.text
            else:
                fail.append(i+1)
        # os.remove(filename)
        if fail:
            return text('<center><h2>失败行数'+','.join(fail)+'</h2></center>')
        else:
            return text('<center><h2>全部执行成功</h2></center>')

    else:
        return text('没有上传文件')

from signal import signal, SIGINT
import asyncio
import uvloop
import sys

if __name__ == '__main__':

    try:
        port = int(sys.argv[1])
    except:
        port = 8002
    asyncio.set_event_loop(uvloop.new_event_loop())
    server = app.create_server(host="0.0.0.0", port=port, return_asyncio_server=True, debug=True)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)
    signal(SIGINT, lambda s, f: loop.stop())
    try:
        loop.run_forever()
    except:
        loop.stop()
