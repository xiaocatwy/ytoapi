#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: oeder_views.py
@time: 2019/6/22 9:32 PM
@desc:
'''
from aliyunService.ossService import upload_stream
from playhouse.shortcuts import model_to_dict
from sanic.response import text,json_dumps
from services.devices_service import DeviceService
from apps import get_page_data
from sanic import Blueprint, response
agent_devices_bp = Blueprint('reder')
from models.order import Product, DeviceBatchApply,DeviceExtension
from models.agent_do import AgentMerchant
from models.advertise_do import AdvertiseGroup
from models.advertise_profit import AdvertiseProfit
from conf import AGENT_COOKIE_TOKEN
from utils.cookie_util import get_cookies
from base import jinja
import pandas as pd
import numpy as np
import uuid
import csv
import time

@order_bp.route("/order/list", methods=["GET", "POST"])
async def device_list(request):
    """
    条件查询
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 产品
        product = Product.select().filter(Product.deleted == 0)
        # 广告组
        advertise_group = AdvertiseGroup.select().filter(AdvertiseGroup.deleted == 0)
        # 代理人
        device_agent = AgentMerchant.select().filter(AgentMerchant.deleted == 0)
        # APPLY_ID
        apply_id = DeviceBatchApply.select().filter(DeviceBatchApply.deleted == 0)

        cookie = request.cookies.get('agent_user')
        print("当前代理用户返回的cookies为 %s " % cookie)
        agent_dict = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        print(agent_dict)
        username = agent_dict.get('username')
        level = agent_dict.get('level')
        agent_id = request.app.get_id_by_show_id(agent_dict.get('show_id'))
        agents = AgentMerchant.select().filter(AgentMerchant.deleted == 0)
        kargs = {}
        kargs['username'] = username
        kargs['level'] = level
        kargs['agent_id'] = agent_id
        kargs["sn_no"] = request.args.get("sn_no", "")
        kargs["province"] = request.args.get("province", "")
        kargs["area"] = request.args.get("area", "")
        kargs["space_tag"] = request.args.get("space_tag", "")
        kargs["product_name"] = request.args.get("product_name", "")
        kargs["group_name"] = request.args.get("group_name", "")
        kargs["agent_name"] = request.args.get("agent_name", "")
        kargs["apply_id"] = request.args.get("apply_id", "")
        kargs["status"] = request.args.get("status", "")
        kargs["produce_version"] = request.args.get("produce_no", "")
        # query = DeviceService().query_list(**kargs)
        query = DeviceService().query_child_device(agent_id)
        page = get_page_data(request, query)

        data = {"render": page.render(), "result": []}
        for i in page.result:
            one_result = model_to_dict(i)
            # 代理
            if i.agent_id == 0:
                one_result["agent_company"] = "无"
            else:
                agent = AgentMerchant.get(AgentMerchant.id == i.agent_id)
                one_result["agent_company"] = agent.agent_company
            # # 广告组
            # if i.advertise_group_id == 0:
            #     one_result["group_name"] = "无"
            # else:
            #     group = AdvertiseGroup.get(AdvertiseGroup.id == i.advertise_group_id)
            #     one_result["group_name"] = group.group_name
            # 分成
            if i.profit_id == 0:
                one_result["profit_name"] = "无"
            else:
                profit = AdvertiseProfit.get(AdvertiseProfit.id == i.profit_id)
                one_result["profit_name"] = profit.profit_name
            data["result"].append(one_result)
        return jinja.render("agent/device-list.html", request, data=data, kargs=kargs, products=product, agents=device_agent,
                            groups=advertise_group, apply_ids=apply_id)
    # 删除
    elif request.method == "POST":
        id = request.form.get("id")
        Devices.update({Devices.deleted: 1}).where(Devices.id == id).execute()
        device = Devices.select().filter(Devices.id == id).get()
        agent_id = device.agent_id
        if agent_id != 0:
            id = AgentMerchant.select().filter(AgentMerchant.id == agent_id).get()
            AgentMerchant.update({AgentMerchant.device_count: int(id.device_count)-1}).where(AgentMerchant.id == id).execute()
        return response.redirect('/agent_device/list')


# 添加
@agent_devices_bp.route("/agent_device/add", methods=['GET', 'POST'])
async def device_add(request):
    if request.method == 'GET':
        data = Product.select().filter(Product.deleted == 0)
        agent = AgentMerchant.select().filter(AgentMerchant.deleted == 0)
        profit = AdvertiseProfit.select().filter(AdvertiseProfit.deleted == 0)
        group = AdvertiseGroup.select().filter(AdvertiseGroup.deleted == 0)
        return jinja.render("agent/device-add.html", request, data=data, agent=agent, group=group, profit=profit)
    elif request.method == "POST":
        data = request.form
        if not request.files.get("qrcode_img"):
            data["qrcode_img"] = ["无"]
        else:
            img_file = request.files.get('qrcode_img')
            file_parameters = {
                'body': img_file.body,
                'name': img_file.name,
                'type': img_file.type,
            }
            is_sucess, img_url = upload_stream(file_parameters)
            data["qrcode_img"] = [img_url]
        user = request.app.user
        data["username"] = [user.get("username", "")]
        DeviceService().add_device(data)
        return response.redirect('/agent_device/list')


# 批量添加
@agent_devices_bp.route("/agent_device/add_list", methods=['GET', 'POST'])
async def device_add_list(request):
    if request.method == 'GET':
        data = Product.select().filter(Product.deleted==0)
        return jinja.render("agent/device-add-list.html", request, data=data)
    elif request.method == "POST":
        data = request.form
        user = request.app.user
        data["username"] = [user.get("username", "")]
        DeviceService().add_list_device(data)
        return response.redirect('/agent_device/list')


# 更新
@agent_devices_bp.route("/agent_device/<show_id>", methods=['GET', 'POST'])
async def device_update(request, show_id):
    '''
    更新设备
    :param request:
    :param show_id:
    :return:
    '''
    if request.method == 'GET':
        agent = AgentMerchant.select().filter(AgentMerchant.deleted == 0)
        group = AdvertiseGroup.select().filter(AdvertiseGroup.deleted == 0)
        profit = AdvertiseProfit.select().filter(AdvertiseProfit.deleted == 0)
        data = Devices.select().filter(Devices.id == show_id).get()
        data = model_to_dict(data)
        return jinja.render("agent/device-updata.html", request, data=data, agent=agent, group=group, profit=profit)
    elif request.method == 'POST':
        user = request.app.user
        data = request.form
        data["updata_user"] = [user.get("username", "")]
        data["update_time"] = [time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))]
        if not request.files.get("qrcode_img"):
            del data["qrcode_img"]
        else:
            img_file = request.files.get('qrcode_img')
            file_parameters = {
                'body': img_file.body,
                'name': img_file.name,
                'type': img_file.type,
            }
            is_sucess, img_url = upload_stream(file_parameters)
            data["qrcode_img"] = [img_url]
        kargs = {key: value[0] for key, value in data.items()}
        old_device = Devices.select().filter(Devices.id == show_id).get()
        old_agent_id = old_device.agent_id
        agent_id = kargs.get("agent_id","")
        if agent_id == "" or agent_id == old_agent_id or agent_id=="0":
            DeviceService().update_device(show_id, **kargs)
        else:
            add_id = AgentMerchant.select().filter(AgentMerchant.id == agent_id).get()
            AgentMerchant.update({AgentMerchant.device_count: int(add_id.device_count)+1}).where(
                AgentMerchant.id == add_id).execute()
            minus = AgentMerchant.select().filter(AgentMerchant.id == old_agent_id)
            if minus:
                minus_id = minus.get()
                AgentMerchant.update({AgentMerchant.device_count: int(minus_id.device_count)-1}).where(
                    AgentMerchant.id == minus_id).execute()
            DeviceService().update_device(show_id, **kargs)

        return text('修改完成')


# 设备状态更新
@agent_devices_bp.route("/agent_device/status", methods=['GET', 'POST'])
async def device_update(request):
    if request.method == 'GET':
        show_id = request.args.get("show_id")
        data = Devices.select().filter(Devices.show_id == int(show_id)).get()
        data = model_to_dict(data)
        return jinja.render("agent/device-used.html", request, data=data)
    if request.method == 'POST':
        data = request.form
        show_id = data.get('show_id',"")
        kargs = {key: value[0] for key, value in data.items()}
        Devices.update(**kargs).where(Devices.show_id == show_id).execute()
        return text('修改完成')


# 导出设备
from models.order import Devices
@agent_devices_bp.route("/agent_device/out", methods=['GET', 'POST'])
@agent_devices_bp.route("/agent_device/export", methods=['GET', 'POST'])
async def device_out(request):
    if request.method == 'GET':
        kargs = {}
        kargs["sn_no"] = request.args.get("sn_no", "")
        kargs["province"] = request.args.get("province", "")
        kargs["area"] = request.args.get("area", "")
        kargs["space_tag"] = request.args.get("space_tag", "")
        kargs["product_name"] = request.args.get("product_name", "")
        kargs["group_name"] = request.args.get("group_name", "")
        kargs["agent_name"] = request.args.get("agent_name", "")
        kargs["apply_id"] = request.args.get("apply_id", "")
        kargs["status"] = request.args.get("status", "")
        query = DeviceService().query_list(**kargs)

        file_name = str(uuid.uuid4())
        file_path = "out_excel/"+file_name+".csv"
        with open(file_path, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            columns = ["device_name", "advertise_group_id", "agent_id", "profit_id"]
            spamwriter.writerow(columns)
            for i in query:
                sn_no_list = [i.device_name, "", "", "", "", ""]
                spamwriter.writerow(sn_no_list)
        # excel = pd.DataFrame(np.array(array))#, columns=[u"设备编号", u"安装省份", u"安装城市", u"安装区域", u"详细地址", u"安装场景"])
        #
        # excel.to_excel(file_path,index=False)
        # print(file_path)
        return await response.file_stream(file_path,filename=file_name+".csv",chunk_size=1024)

# 导入设备
@agent_devices_bp.route("/agent_device/up", methods=['GET', 'POST'])
@agent_devices_bp.route("/agent_device/import", methods=['GET', 'POST'])
async def device_inter(request):
    if request.method == 'GET':
        return jinja.render('agent/device_up_excel.html', request)
    else:
        test_file = request.files.get('excel')
        print(test_file.type)
        df = pd.read_csv(test_file.body)
        print(df)
        # 替换nan
        df = df.where(df.notnull(), "")
        # 矩阵
        data = np.array(df)
        for i in data:
            # 改成字典
            kargs = {}
            kargs["advertise_group_id"] = i[1]
            kargs["agent_id"] = i[2]
            kargs["profit_id"] = i[3]
            Devices.update(**kargs).where(Devices.device_name == i[0]).execute()
        return text('已导入')




@agent_devices_bp.route("/agent_device/ajax/list", methods=["GET", "POST"])
async def device_ajax_list(request):
    """
    条件查询
    :param request:
    :return:
    """

    product = Product.select().filter(Product.deleted == 0)
    # 广告组
    advertise_group = AdvertiseGroup.select().filter(AdvertiseGroup.deleted == 0)
    # 代理人
    device_agent = AgentMerchant.select().filter(AgentMerchant.deleted == 0)
    # APPLY_ID
    apply_id = DeviceBatchApply.select().filter(DeviceBatchApply.deleted == 0)

    kargs = {}
    kargs["sn_no"] = request.args.get("sn_no", "")
    kargs["province"] = request.args.get("province", "")
    kargs["area"] = request.args.get("area", "")
    kargs["space_tag"] = request.args.get("space_tag", "")
    kargs["product_name"] = request.args.get("product_name", "")
    kargs["group_name"] = request.args.get("group_name", "")
    kargs["agent_name"] = request.args.get("agent_name", "")
    kargs["apply_id"] = request.args.get("apply_id", "")
    kargs["status"] = request.args.get("status", "")
    query = DeviceService().query_list(**kargs)
    page = get_page_data(request, query)

    data = {"render": page.render(), "result": []}
    for i in page.result:
        one_result = model_to_dict(i)
        # 代理
        if i.agent_id == 0:
            one_result["agent_company"] = "无"
        else:
            agent = AgentMerchant.get(AgentMerchant.id == i.agent_id)
            one_result["agent_company"] = agent.agent_company
        # 广告组
        if i.advertise_group_id == 0:
            one_result["group_name"] = "无"
        else:
            group = AdvertiseGroup.get(AdvertiseGroup.id == i.advertise_group_id)
            one_result["group_name"] = group.group_name
        # 分成
        if i.profit_id == 0:
            one_result["profit_name"] = "无"
        else:
            profit = AdvertiseProfit.get(AdvertiseProfit.id == i.profit_id)
            one_result["profit_name"] = profit.profit_name
        data["result"].append(one_result)

    page_html = jinja.render_string("agent/ajax_device_list.html", request, data=data, kargs=kargs, products=product, agents=device_agent,
                    groups=advertise_group, apply_ids=apply_id)

    return text(page_html)