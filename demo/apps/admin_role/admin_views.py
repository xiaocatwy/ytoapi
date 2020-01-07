

# from models.user import Admins
# from playhouse.shortcuts import model_to_dict
# from sanic.views import HTTPMethodView
# from sanic.response import text
# from models.order import Devices
# from services.admin_services import AdminService
# from apps import get_page_data
# from sanic import Blueprint, response
# from middleware.authorized import authorized
# admin_bp = Blueprint('admin')
#
# from base import jinja
#
#
# @admin_bp.route("/admin/list", methods=["GET","POST"])
# @authorized()
# async def admin_list(request):
#     '''
#     后台人员列表
#     :param request:
#     :return:
#     '''
#     if request.method == 'GET':
#         kargs = {}
#         # kargs["product_name"] = request.args.get("product_name", "")
#         query = AdminService().query_list(kargs)
#         page = get_page_data(request, query)
#         return jinja.render("admin/role-list.html", request, data=page, kargs=kargs)
#     # 删除
#     elif request.method == "POST":
#         id = request.form.get("id")
#         Admins.delete().where(Admins.show_id == str(id)).execute()
#         return text("已删除")
#
#
# # 添加
# @admin_bp.route("/admin/add", methods=['GET', 'POST'])
# @authorized()
# async def admin_add(request):
#     if request.method == 'GET':
#         return jinja.render("admin/role-add.html", request)
#     elif request.method == "POST":
#         # data = dict(request.query_args)
#         data = request.form
#         permision_list=""
#         if "总权限" in data.keys():
#             permision_list+="总权限,"
#         if "设备权限" in data.keys():
#             permision_list+="设备权限,"
#         if "广告权限"in data.keys():
#             permision_list+="广告权限,"
#         if "分成权限"in data.keys():
#             permision_list+="分成权限,"
#         if "代理权限" in data.keys():
#             permision_list+="代理权限,"
#         if "财务权限" in data.keys():
#             permision_list+="财务权限,"
#         data["permision_list"]=[permision_list[:-1]]
#         AdminService().add_admin(data)
#         return text("已添加")
#
# # 更新
# @admin_bp.route("/admin/<show_id>", methods=['GET', 'POST'])
# @authorized()
# async def device_update(request, show_id):
#     if request.method == 'GET':
#         data = Admins.select().filter(Admins.show_id == show_id).get()
#         data = model_to_dict(data)
#         permision = data["permision_list"].split(",")
#         data["permision_list"] = permision
#         return jinja.render("admin/role-update.html", request, data=data)
#     elif request.method == 'POST':
#         data = request.form
#         permision_list = ""
#         if "总权限" in data.keys():
#             permision_list += "总权限,"
#         if "设备权限" in data.keys():
#             permision_list += "设备权限,"
#         if "广告权限" in data.keys():
#             permision_list += "广告权限,"
#         if "分成权限" in data.keys():
#             permision_list += "分成权限,"
#         if "代理权限" in data.keys():
#             permision_list += "代理权限,"
#         if "财务权限" in data.keys():
#             permision_list += "财务权限,"
#         data["permision_list"] = [permision_list[:-1]]
#         AdminService().update_admin(show_id, data)
#         return text('修改完成')
#
#
#
#
