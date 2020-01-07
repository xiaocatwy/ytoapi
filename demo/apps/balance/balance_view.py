from sanic.response import text
import time
from middleware.authorized import authorized
from services.user_service import UserService
from apps import get_page_data
from sanic import Blueprint, response
balance_bp = Blueprint('balance')
from models.money import Balance, Commission
from conf import AGENT_COOKIE_TOKEN
from utils.cookie_util import get_cookies
from base import jinja


@balance_bp.route("/balance/all/list")
@authorized()
async def balance_list(request):
    kargs={}
    kargs['id'] = request.args.get("id", "")
    kargs['phone'] = request.args.get("phone", "")
    kargs["username"] = request.args.get("username", "")
    query = Balance().filter(Balance.deleted==0)
    if "id" in kargs and kargs.get('id').strip():
        query = query.filter(user_id=int(kargs["id"]))
    if "username" in kargs and kargs.get('username').strip():
        query = query.filter(username=kargs["username"])
    if "phone" in kargs and kargs.get("phone").strip():
        query = query.filter(phone=kargs["phone"])
    data = get_page_data(request, query)
    return jinja.render("admin/balance_all_list.html", request, data=data, kargs=kargs)


@balance_bp.route("/balance/list")
@authorized()
async def balance_list(request):
    cookie = request.cookies.get("user")
    user = get_cookies(AGENT_COOKIE_TOKEN,cookie)
    phone = user.get('phone')
    user_id = user.get('id')
    data = Balance().filter(Balance.user_id==user_id,Balance.phone==phone)
    return jinja.render("admin/balance-list.html", request, data=data)


#支付宝初始化
from alipay import AliPay
app_private_key_string = open("alipay/private_key_2048.txt").read()
alipay_public_key_string = open("alipay/alipay_pub_key").read()

app_notify_url="http://yto.youhaozhi.com/alipay/notify"
_alipay = AliPay(
    appid="2019082666427588",
    app_notify_url=app_notify_url,
    # app_private_key_path="pay_key/private_2048.txt",
    # alipay_public_key_path="pay_key/public_2048.txt"
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string
)

from models.user import PayOrders, Users


@balance_bp.route("/balance/add", methods=["GET","POST"])
@authorized()
async def balance_add(request):
    if request.method == 'GET':
        return jinja.render("admin/balance-add.html", request,message='')
    if request.method == "POST":
        money = request.form.get("money")
        try:
            float(money)
        except:
            return jinja.render("admin/balance-add.html", request,message="输入金额错误")
        cookie = request.cookies.get("user")
        user = get_cookies(AGENT_COOKIE_TOKEN, cookie)
        user_id = user.get('id')
        pay_orders = PayOrders()
        pay_orders.user_id = user_id
        pay_orders.product = '单号储值{0}'.format(money)
        pay_orders.out_trade_no =str(int(time.time()*1000))+str(user_id)
        pay_orders.total_fee=float(money)
        pay_orders.status = 0
        pay_orders.notify_url=app_notify_url

        order_string = _alipay.api_alipay_trade_page_pay(out_trade_no=pay_orders.out_trade_no,
                                                        total_amount=money,
                                                        subject=pay_orders.product)
        pay_orders.ali_pay_str = order_string
        pay_orders.save()
        return response.redirect('https://openapi.alipay.com/gateway.do?'+order_string)
        # a = True
        # if a:
        #     old = Balance().get(Balance.user_id==user_id,Balance.phone==phone)
        #     Balance().update({"amount":old.amount+float(money)}).where(Balance.user_id == user_id,Balance.phone==phone).execute()
        #     return text("已充值")
        # else:
        #     return text("充值失败")

#支付回调
from models.user import PayOrders
@balance_bp.route("/alipay/notify",methods=['POST','GET'])
async def alipay_notify(request):
    if request.method=='POST':
        _data = request.form
        data={}
        for key in _data.keys():
            data.update({key:_data.get(key)})
        signature = data.pop("sign")
        # verify
        success = _alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS","TRADE_FINISHED"):
            invoice_amount = float(data['invoice_amount'])
            trade_no = data.get('out_trade_no')
            order = PayOrders.get(PayOrders.out_trade_no==trade_no)
            user_id = order.user_id
            if order.status==0:
                order.status = 1
                order.save()
                old = Balance().get(Balance.user_id==user_id)
                Balance().update({"amount":old.amount+float(invoice_amount)}).where(Balance.user_id == user_id).execute()
                # 首次充值邀请加10元
                if PayOrders().filter(PayOrders.user_id==user_id,PayOrders.status==1).count()==1:
                    user = Users().get(Users.id == user_id)
                    if user.agent_id !=0:
                        detail = "你邀请ID为{}的首冲奖励".format(user_id)
                        Commission().create(user_id=user.agent_id, from_user_id=user_id,
                                            once_amount=10, detail=detail)
                        agent_old_balance = Balance.get(Balance.user_id == user.agent_id)
                        Balance().update({Balance.commission: agent_old_balance.commission + 10}).where(
                            Balance.user_id == user.agent_id).execute()




            return response.html("<html><center><h1>支付成功</h2></center></html>")
        else:
            return response.html("<html><center><h1>支付失败</h2></center></html>")
    else:
        data = dict(request.query_args)
        signature = data.pop("sign")
        success = _alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS","TRADE_FINISHED"):
            trade_no = data.get('out_trade_no')
            order = PayOrders.get(PayOrders.out_trade_no==trade_no)
            if order.status==0:
                order.status = 1
                order.save()
            return response.html("<html><center><h1>支付成功</h2></center></html>")
        else:
            return response.html("<html><center><h1>支付失败</h2></center></html>")

