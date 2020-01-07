# ytoapi

#### 下单接口
>method:POST
>url:/common/order/model

参数 |类型 |是否必须|备注
:-----:|----|----|----
sender_name|str|必须|寄件人 
sender_mobile|str|必须|寄件人电话
sender_prov|string|必须|寄件人省份
sender_city|string|必须|寄件人城市
sender_address|string|必须|寄件人地址 
recive_name|str|必须|收件人 
recive_mobile|str|必须|收件人电话
recive_prov|string|必须|收件人省份
recive_city|string|必须|收件人城市
recive_address|string|必须|收件人地址
itemName|string|必须|产品名称 
number|int|必须|产品数量
itemValue|float|非|产品价值

weight|float|非|重量 

>>itemName,number,itemValue可以为多组

返回值用例
```json
{
    "code": 1,
    "data":{'logisticProviderID': 'YTO', 'txLogisticID': '1564125994502677341', 'clientID': 'K11122126', 'mailNo': '822146391430', 'code': '200', 'success': 'true', 'distributeInfo': {'shortAddress': '', 'consigneeBranchCode': '', 'packageCenterCode': '571926', 'packageCenterName': '区域件'}}
}
```

