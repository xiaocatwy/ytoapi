#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: oeder_views.py
@time: 2019/6/22 9:32 PM
@desc:
'''

from apps import get_page_data
from playhouse.shortcuts import model_to_dict
from sanic import Blueprint, response
from services.order_service import OrderService

from conf import AGENT_COOKIE_TOKEN
from utils.cookie_util import get_cookies

order_bp = Blueprint('order')
from models.order import UserLogistic
from base import jinja
from apps import sender
from apps import recive
from apps import config
from apps import signatral
from apps import custom_root
import random
from models.user import SendAddress, Users
from sanic.response import text, json
from dicttoxml import dicttoxml
import xmltodict
import requests
import urllib
import xlrd
import time
from middleware.authorized import authorized


@order_bp.route("/order/list", methods=["GET", "POST"])
@authorized()
async def order_list(request):
    """
订单列表
:param request:
:return:
"""
    if request.method == 'GET':
        users = request.app.user
        kargs = {}
        kargs["mailNo"] = request.args.get("mailNo", "")
        kargs["sender_name"] = request.args.get("sender_name", "")
        kargs["sender_mobile"] = request.args.get("sender_mobile", "")
        kargs["recive_name"] = request.args.get("recive_name", "")
        kargs["recive_mobile"] = request.args.get("recive_mobile", "")
        query = OrderService().query_list(users, **kargs)
        data = get_page_data(request, query)
        return jinja.render("admin/order-list.html", request, kargs=kargs, data=data)

# 解析
@order_bp.route("/copy/content", methods=["POST"])
@authorized()
async def copy_content(request):
    if request.method=="POST":
        data = request.form

        content=data.get("content","")
        content_list=content.split("，")
        if len(content_list)==1:
            content_list=content.split(",")
        area_list = content_list[2].split()
        return json({"name":content_list[0],"phone":content_list[1],"province":area_list[0],
                     "city":area_list[1],"address":area_list[2]+area_list[3]+area_list[4]})


# 下单
from models.money import Balance, Commission


@order_bp.route("/order/add", methods=['GET', 'POST'])
@authorized()
async def order_add(request):
    if request.method == 'GET':
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get("id")
        area = SendAddress.get(SendAddress.deleted == 0,SendAddress.user_id == user_id)
        orders = UserLogistic.select().filter(UserLogistic.deleted == 0, UserLogistic.user_id == user_id).order_by(
            UserLogistic.create_time.desc())
        old_balance = Balance.get(Balance.user_id == user_id)
        if orders.count() > 0:
            order = orders[0]
            data = orders[0]
        else:
            order = None
            data = None
        if old_balance.amount<1.8:
            return response.html('<html><center><h1>余额不足,请充值   <a href="/balance/add" target="_blank">点击充值</a></h1></center></html>')
        else:
            if order and order.items:
                items = order.items.split('-')
                try:
                    item = [it.split(":")[1] for it in items]
                except:
                    item = []
            else:
                item = []
            return jinja.render("/admin/order-add.html", request,area=area, data=data, item=item)
    elif request.method == "POST":
        data = request.form
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get("id")
        if not user.get('is_admin'):
            balance = Balance.get(Balance.user_id==user_id)
            if balance and balance.amount<1.8:
                return response.html('<html><center><h1>余额不足,请充值   <a href="/balance/add">点击充值</a></h1></center></html>')
        keys = ['sender_name', 'sender_mobile', 'sender_prov', 'sender_city', 'sender_address',
                'recive_name', 'recive_mobile', 'recive_prov', 'recive_city', 'recive_address',
                'itemName', 'number']
        for key in keys:
            if not request.form.get(key, '').strip():
                return json({'code': 0, 'msg': '参数{0}'.format(key) + '不能为空'})
            if len(request.form.get(key)) > 256:
                return json({'code': 0, 'msg': '参数{0}'.format(key) + '长度不能超过256'})
        params = request.form
        sender.update(
            {"name": params.get('sender_name'), "mobile": params.get('sender_mobile'),
             "prov": params.get('sender_prov'),
             "city": params.get('sender_city'), "address": params.get('sender_address')})
        recive.update(
            {"name": params.get('recive_name'), "mobile": params.get('recive_mobile'),
             "prov": params.get('recive_prov'),
             "city": params.get('recive_city'), "address": params.get('recive_address')})

        items = []
        itemNames = request.form.get('itemName')
        numbers = request.form.get('number')
        itemValues = request.form.get('itemValue')
        weight = request.form.get('weight')

        items.append({"itemName": itemNames, "number": numbers, "itemValue": itemValues, "weight": weight})
        order_id = str(int(time.time() * 1000000)) + str(random.randint(10, 1000))
        data = {'clientID': config.get('ClientID'), 'logisticProviderID': 'YTO',
                'customerId': config.get('ClientID'), 'txLogisticID': order_id,
                'tradeNo': '', 'orderType': 1, 'serviceType': 0,
                'itemsWeight': 0.0, 'flag': 0, 'goodsValue': 0, 'special': 0,
                'insuranceValue': 0.0, 'totalServiceFee': 0.0, 'codSplitFee': 0.0}
        data.update({"sender": sender, "receiver": recive, 'items': items})
        xml_body = dicttoxml(data, root=True, custom_root=custom_root, attr_type=False)
        xml_body = xml_body.decode().replace('<?xml version="1.0" encoding="UTF-8" ?>', '')
        # xml_body='<RequestOrder><clientID>K11122126</clientID><logisticProviderID>YTO</logisticProviderID><customerId>K11122126</customerId><txLogisticID>K11122126abc1004</txLogisticID><tradeNo>K11122126</tradeNo><orderType>1</orderType><serviceType>0</serviceType><itemsWeight>1.2</itemsWeight><flag>0</flag><goodsValue>0</goodsValue><special>0</special><insuranceValue>0.0</insuranceValue><totalServiceFee>0.0</totalServiceFee><codSplitFee>0.0</codSplitFee><sender><name>张三</name><mobile>13550031574</mobile><prov>浙江省</prov><city>杭州市</city><address>滨江区网商路599号</address></sender><receiver><name>李四</name><mobile>13550031578</mobile><prov>四川省</prov><city>成都市</city><address>龙泉驿区西河镇</address></receiver><items><item><itemName>男式衣服</itemName><number>1</number><itemValue>25</itemValue></item></items></RequestOrder>'
        data_digest = signatral(xml_body, config.get('ClientSec'))
        # print(data_digest)
        # data_digest='E9yeCCnxCFLmQs8bHM+oZQ=='
        params = {'clientId': config.get('ClientID'), 'data_digest': data_digest, 'logistics_interface': xml_body}
        # data = urllib.parse.urlencode(params)
        config.get('UrlOrder') + '?' + urllib.parse.urlencode(params)
        # print(urllib.parse.urlencode(params))
        res = requests.post(config.get('UrlOrder') + '?' + urllib.parse.urlencode(params))
        content = res.text
        res_data = xmltodict.parse(content)
        level = request.app.user.get('level', 0)
        if level == 1:
            level_proce = 1.8
        if level == 2:
            level_proce = 1.5
        if res_data.get('Response').get('success') in ('true', True):
            address = res_data['Response'].pop('distributeInfo')
            res_data = dict(res_data['Response'].items())
            res_data.update({'distributeInfo': dict(address)})
            res_data.update(data)
            old_shop = [i['itemName'] + ',' + i['number'] + ',' + i['itemValue'] for i in res_data.get('items')]
            shop = old_shop[0].split(",")
            kargs = {'user_id': user_id, 'logisticProviderID': res_data.get('logisticProviderID', ''),
                     'txLogisticID': res_data.get('txLogisticID', ''), 'clientID': res_data.get('clientID', ''),
                     'mailNo': res_data.get('mailNo', ''), 'customerId': res_data.get('customerId', ''),
                     'tradeNo': res_data.get('tradeNo', ''), 'orderType': res_data.get('orderType', ''),
                     'serviceType': res_data.get('serviceType'), 'itemsWeight': res_data.get('itemsWeight'),
                     'flag': res_data.get('flag'),
                     'goodsValue': res_data.get('goodsValue', ''), 'special': res_data.get('special', ''),
                     'insuranceValue': res_data.get('insuranceValue', ''),
                     'totalServiceFee': res_data.get('totalServiceFee', ''),
                     'codSplitFee': res_data.get('codSplitFee', ''),
                     'sender_name': res_data.get('sender').get('name', ''),
                     'sender_mobile': res_data.get('sender').get('mobile', ''),
                     'sender_prov': res_data.get('sender').get('prov', ''),
                     'sender_city': res_data.get('sender').get('city', ''),
                     'sender_address': res_data.get('sender').get('address', ''),
                     'recive_name': res_data.get('receiver').get('name', ''),
                     'recive_mobile': res_data.get('receiver').get('mobile', ''),
                     'recive_prov': res_data.get('receiver').get('prov', ''),
                     'recive_city': res_data.get('receiver').get('city', ''),
                     'recive_address': res_data.get('receiver').get('address', ''),
                     'items': "名称:{}-数量:{}-价值:{}".format(shop[0], shop[1], shop[2]), "weight": weight,
                     "price": level_proce}
            UserLogistic.create(**kargs)
            # 减余额
            if not user.get('is_admin'):
                old_balance = Balance.get(Balance.user_id == user_id)
                Balance().update({Balance.amount:old_balance.amount-level_proce}).where(Balance.user_id == user_id).execute()

            # 佣金操作
            order_user = Users.get(Users.id == user_id)
            if order_user.agent_id != 0:
                once_amount = level_proce*0.05
                detail = "你邀请ID为{}的下单奖励".format(user_id)
                Commission().create(user_id=order_user.agent_id,from_user_id=user_id,once_amount=once_amount,detail=detail)
                agent_old_balance = Balance.get(Balance.user_id == order_user.agent_id)
                Balance().update({Balance.commission: agent_old_balance.commission + once_amount}).where(
                    Balance.user_id == order_user.agent_id).execute()


            # 存库
            if request.form.get('weight', ''):
                paramSetWeight = {'waybillNo': order_id, 'weight': weight, 'customerCode': config.get('ClientID'),
                                  'clientId': config.get('WeightSec')}
                req = requests.get(config.get('UrlWeight'), params=paramSetWeight)
                w_text = req.text
            content = """
                    <html>
                    <script>
                    alert("下单成功");
                    window.location.href='http://{0}/order/add';
                    </script>
                    </html>
                    """.format(request.host)
            return response.html(content)

        else:
            # data = dict(res_data['Response'].items())
            # return json({'code': 0, 'data': data})
            content = """
                    <html>
                    <script>
                    alert("下单失败");
                    window.location.href='http://{0}/order/add';
                    </script>
                    </html>
                    """.format(request.host)
            return response.html(content)

@order_bp.route('/order/download',methods =['GET','POST'])
@authorized()
async def excel_download(request):
    return await response.file_stream("圆通单号模板.xls", filename="圆通单号模板.xls")


@order_bp.route('/order/upload',methods=['GET','POST'])
@authorized()
async def excel_upload(request):
    if request.method == 'GET':
        return jinja.render("admin/excel.html", request)
    else:
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get("id")

        img_file = request.files.get('ytofile')
        if img_file:
            file_parameters = {
                'body': img_file.body,
                'name': img_file.name,
                'type': img_file.type,
            }
            filename = img_file.name
            f = open(filename, 'wb')
            f.write(img_file.body)
            f.close()
            # 只能读不能写
            book = xlrd.open_workbook(filename)  # 打开一个excel
            sheet = book.sheet_by_index(0)  # 根据顺序获取sheet

            if not user.get('is_admin'):
                balance = Balance.get(Balance.user_id == user_id)
                if balance and balance.amount < 1.8*sheet.nrows:
                    return response.html('<html><center><h1>余额不足,请充值   <a href="/balance/add">点击充值</a></h1></center></html>')
            fail = []
            level_proce = ""
            area = SendAddress.get(SendAddress.user_id == user_id, SendAddress.deleted==0)
            for i in range(sheet.nrows):
                if i == 0:
                    continue
                row_values = sheet.row_values(i)
                if area and not row_values[0]:
                    name = area.sender_name
                else:
                    name = row_values[0]
                if area and not row_values[1]:
                    mobile = area.sender_mobile
                else:
                    mobile = row_values[1]
                if area and not row_values[2]:
                    prov = area.sender_prov
                else:
                    prov = row_values[2]
                if area and not row_values[3]:
                    city = area.sender_city
                else:
                    city = row_values[3]
                if area and not row_values[4]:
                    address = area.sender_address
                else:
                    address = row_values[4]
                sender = {"name": name, "mobile": mobile, "prov": prov, "city": city,
                          "address": address}
                recive = {"name": row_values[5], "mobile": row_values[6], "prov": row_values[7], "city": row_values[8],
                          "address": row_values[9]}
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
                params = {'clientId': config.get('ClientID'), 'data_digest': data_digest,
                          'logistics_interface': xml_body}
                config.get('UrlOrder') + '?' + urllib.parse.urlencode(params)
                res = requests.post(config.get('UrlOrder') + '?' + urllib.parse.urlencode(params))
                content = res.text
                res_data = xmltodict.parse(content)
                level = request.app.user.get('level', 0)
                if level == 1:
                    level_proce = 1.8
                if level == 2:
                    level_proce = 1.5
                if res_data.get('Response').get('success') in ('true', True):
                    address = res_data['Response'].pop('distributeInfo')
                    res_data = dict(res_data['Response'].items())
                    res_data.update({'distributeInfo': dict(address)})
                    res_data.update(data)
                    kargs = {'user_id': user_id, 'logisticProviderID': res_data.get('logisticProviderID', ''),
                             'txLogisticID': res_data.get('txLogisticID', ''), 'clientID': res_data.get('clientID', ''),
                             'mailNo': res_data.get('mailNo', ''), 'customerId': res_data.get('customerId', ''),
                             'tradeNo': res_data.get('tradeNo', ''), 'orderType': res_data.get('orderType', ''),
                             'serviceType': res_data.get('serviceType', ''),
                             'itemsWeight': res_data.get('itemsWeight', ''),
                             'flag': res_data.get('flag', ''),
                             'goodsValue': res_data.get('goodsValue', ''), 'special': res_data.get('special', ''),
                             'insuranceValue': res_data.get('insuranceValue', ''),
                             'totalServiceFee': res_data.get('totalServiceFee', ''),
                             'codSplitFee': res_data.get('codSplitFee', ''),
                             'sender_name': res_data.get('sender').get('name', ''),
                             'sender_mobile': str(int(res_data.get('sender').get('mobile', ''))),
                             'sender_prov': res_data.get('sender').get('prov', ''),
                             'sender_city': res_data.get('sender').get('city', ''),
                             'sender_address': res_data.get('sender').get('address', ''),
                             'recive_name': res_data.get('receiver').get('name', ''),
                             'recive_mobile': str(int(res_data.get('receiver').get('mobile', ''))),
                             'recive_prov': res_data.get('receiver').get('prov', ''),
                             'recive_city': res_data.get('receiver').get('city', ''),
                             'recive_address': res_data.get('receiver').get('address', ''),
                             'items': "名称:{}-数量:{}-价值:{}".format(items[0]["itemName"], items[0]["number"],
                                                                 items[0]["itemValue"]), "weight": weight,
                             "price": level_proce}
                    UserLogistic.create(**kargs)
                    if not user.get('is_admin'):
                        old_balance = Balance.get(Balance.user_id == user_id)
                        Balance().update({Balance.amount: old_balance.amount - level_proce}).where(
                            Balance.user_id == user_id).execute()

                    # 佣金操作
                    order_user = Users.get(Users.id == user_id)
                    if order_user.agent_id != 0:
                        once_amount = level_proce * 0.05
                        detail = "你邀请ID为{}的下单奖励".format(user_id)
                        Commission().create(user_id=order_user.agent_id, from_user_id=user_id,
                                            once_amount=once_amount, detail=detail)
                        agent_old_balance = Balance.get(Balance.user_id == order_user.agent_id)
                        Balance().update({Balance.commission: agent_old_balance.commission + once_amount}).where(
                            Balance.user_id == order_user.agent_id).execute()
                    # if request.form.get('weight', ''):
                    #     paramSetWeight = {'waybillNo': order_id, 'weight':weight, 'customerCode': config.get('ClientID'),
                    #                       'clientId': config.get('WeightSec')}
                    #     req = requests.get(config.get('UrlWeight'), params=paramSetWeight)
                    #     w_text = req.texts
                else:
                    fail.append(i + 1)
            if fail:
                return text('失败行数')
            else:
                return text('全部执行成功')

        else:
            return text('没有上传文件')
