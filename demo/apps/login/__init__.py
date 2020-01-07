# import hashlib
# m = hashlib.md5()
# # 3次加密
# m.update(bytes(hashlib.md5(bytes(hashlib.md5(bytes("123456", encoding="UTF-8")).hexdigest(), encoding="UTF-8")).hexdigest(),
#                encoding="UTF-8"))
# print(m.hexdigest())