import io
import time
import tkinter as tk

import requests
import openpyxl
from PIL import ImageTk, Image
from tinydb import TinyDB, where, Query

from viptool import VipShopUser, BrowserWeb

# TODO: 初始化浏览器
browser = BrowserWeb()

# 加载数据表
db = TinyDB("database.json")
dbq = Query()
users = db.table("users")
orders = db.table("orders")
details = db.table("details")


def update_orders():
    for user in users.search(where("status") == True):
        data = VipShopUser(uid=user["uid"], token=user["token"]).get_orders(page_size=100)
        if data["msg"] == "success":
            for order in data["data"]["orders"]:
                for index_goods in range(len(order["goodsView"])):
                    # 商品编号
                    product_id = order["goodsView"][index_goods]["vSkuId"]
                    # 商品名称
                    product_name = order["goodsView"][index_goods]["name"]
                    # 商品型号
                    product_size = order["goodsView"][index_goods]["sizeName"]
                    # 型号数量
                    product_quantity = order["goodsView"][index_goods]["num"]
                    # 商品价格
                    product_price = order["goodsView"][index_goods]["price"]
                    # 订单号
                    order_id = order["orderSn"]
                    # 用户ID
                    user_id = user["uid"]
                    # 订单状态
                    #   退款完成   97
                    #   已完成     60
                    #   已签收     25
                    #   已发货     22
                    #   订单已取消  97
                    order_status = order["orderStatusName"]
                    # 订单时间
                    # order_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(order["createTime"]))
                    order_time = order["createTime"]
                    # 订单价格
                    order_amount = order["orderAmount"]
                    # 爬取时间
                    # crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    crawl_time = int(time.time())

                    # 如果已存在，只修改状态，否则插入
                    order_target = orders.search((where("order_id") == order_id) & (where("product_id") == product_id))
                    if order_target:
                        orders.update({"order_status": order_status},
                                      (where("order_id") == order_id) & (where("product_id") == product_id))
                    else:
                        orders.insert(
                            {"product_id": product_id, "product_name": product_name, "product_size": product_size,
                             "product_quantity": product_quantity, "product_price": product_price, "order_id": order_id,
                             "user_id": user_id, "order_status": order_status, "order_time": order_time,
                             "order_amount": order_amount, "crawl_time": crawl_time})

    return orders.all()


def update_details():
    for user in users.search(where("status") == True):
        orders_sn = [item['order_id'] for item in orders.search(where("user_id") == user["uid"])]
        check_sn = [item['order_sn'] for item in details.all()]
        for osn in orders_sn:
            # Fixme: 减少请求次数
            if orders_sn in check_sn:
                if time.time() - details.search(where("order_sn") == orders_sn)[0]["order_time"] > 604800:
                    continue
            data = VipShopUser(uid=user["uid"], token=user["token"]).get_details(osn)
            if data["code"] == 200:
                # 订单编号
                order_sn = data["result"]["orderSn"]
                # 订单时间
                order_time = data["result"]["orderTime"]
                # 订单状态
                order_state = data["result"]["orderTrack"]["result"]["currentState"]
                # 用户ID
                user_id = data["result"]["userId"]
                # 订单商品类数
                goods_count = data["result"]["goodsList"]["result"]["goodsTotalCount"]
                # 订单价格
                total_amount = data["result"]["goodsList"]["result"]["totalAmount"]
                # 物流单号
                tracking_sn = data["result"]["orderTrack"]["result"]["orderTrack"][0]["sn"]
                # 物流信息
                tracking_message = data["result"]["orderSummary"]["result"]["message"]
                # 物流电话
                tracking_mobile = data["result"]["orderSummary"]["result"]["mobile"]
                # 物流收件人
                tracking_consignee = data["result"]["orderSummary"]["result"]["consignee"]
                # 物流地址
                tracking_address = data["result"]["orderSummary"]["result"]["areaName"] + \
                                   data["result"]["orderSummary"]["result"]["detailAddress"]
                # 爬取时间
                crawl_time = int(time.time())

                # 如果已存在，只修改状态，否则插入
                order_target = details.search((where("order_sn") == order_sn))
                if order_target:
                    orders.update({"order_state": order_state}, (where("order_sn") == order_sn))
                else:
                    details.insert(
                        {"order_sn": order_sn, "order_time": order_time, "order_state": order_state, "user_id": user_id,
                         "goods_count": goods_count, "total_amount": total_amount, "tracking_sn": tracking_sn,
                         "tracking_message": tracking_message, "tracking_mobile": tracking_mobile,
                         "tracking_consignee": tracking_consignee, "tracking_address": tracking_address,
                         "crawl_time": crawl_time})
    return details.all()


def update_users():
    for _user in users.all():
        if VipShopUser(uid=_user["uid"], token=_user["token"]).is_visible():
            users.update({"status": True, "update_time": int(time.time())}, where("uid") == _user["uid"])
        else:
            users.update({"status": False, "update_time": int(time.time())}, where("uid") == _user["uid"])

    for _user in users.search(where("status") == True):
        user_info = VipShopUser(uid=_user["uid"], token=_user["token"]).get_user_info()["data"]
        users.update(
            {"mobile": user_info["mobile"], "username": user_info["userName"], "nickname": user_info["nickname"],
             "update_time": int(time.time())
             },
            where("uid") == _user["uid"])
    account_list.delete(0, tk.END)

    # 筛洗出有效信息
    for user in users.all():
        user_nsi = {k: v for k, v in user.items() if k in ["username", "remarks", "status", "nickname"]}

        account_list.insert(tk.END,
                            f'{user_nsi["username"]}-{user_nsi["remarks"]}-{"有效" if user_nsi["status"] else "失效"}-{user_nsi["nickname"]}')

    return True


def update_orders_excel():
    """
    导出 excel 的详细内容
    :return:
    """
    data = update_orders()
    crawl_time = data[-1]['crawl_time']
    workbook = openpyxl.Workbook()
    orders_sheet = workbook.active
    orders_sheet.title = f"截至{time.strftime('%Y-%m-%d %H.%M', time.localtime(data[-1]['crawl_time']))}订单数据"

    headers = ["商品编号", "商品名称", "商品规格", "商品数量", "商品价格", "订单编号", "用户编号", "订单状态",
               "下单时间", "订单金额", "抓取时间"]

    for i, header in enumerate(headers):
        orders_sheet.cell(row=1, column=i + 1).value = header

    # 写入数据到工作表中，从第二行开始
    for i, item in enumerate(data):
        # 遍历每个字典的键和值
        for j, (key, value) in enumerate(item.items()):
            # 写入工作表的单元格中，根据键名的顺序和值的类型
            if key in ["order_time", "crawl_time"]:
                orders_sheet.cell(row=i + 2, column=j + 1).value = time.strftime('%Y-%m-%d %H:%M',
                                                                                 time.localtime(value))
            elif key in ["product_price", "order_amount"]:
                orders_sheet.cell(row=i + 2, column=j + 1).value = float(value)
            else:
                orders_sheet.cell(row=i + 2, column=j + 1).value = value
    # 创建用户表
    data = users.all()
    users_sheet = workbook.create_sheet("当前用户状态", 1)
    headers = ["UID", "TOKEN", "状态", "添加时间", "更新时间", "备注", "电话", "用户名", "用户昵称"]
    for i, header in enumerate(headers):
        users_sheet.cell(row=1, column=i + 1).value = header

    for i, item in enumerate(data):
        # 遍历每个字典的键和值
        for j, (key, value) in enumerate(item.items()):
            # 写入工作表的单元格中，根据键名的顺序和值的类型
            if key in ["update_time", "add_time"]:
                users_sheet.cell(row=i + 2, column=j + 1).value = time.strftime('%Y-%m-%d %H:%M',
                                                                                time.localtime(value))
            elif key == "status":
                users_sheet.cell(row=i + 2, column=j + 1).value = "有效账号" if value else "无效账号"
            else:
                users_sheet.cell(row=i + 2, column=j + 1).value = value

    # 保存工作簿到文件中
    workbook.save(f"orders-{time.strftime('%Y年%m月%d日%H时%M分', time.localtime(crawl_time))}.xlsx")
    info.config(
        text=f"导出文件：orders-{time.strftime('%Y年%m月%d日%H时%M分', time.localtime(crawl_time))}.xlsx")


def delete_user():
    """
    删除用户
    :return:
    """
    # 获取选择的用户
    _index = account_list.curselection()

    # 判断是否选择了用户
    if _index:
        # 删除用户
        users.remove(where("uid") == users.all()[_index[0]]["uid"])

    # 更新用户
    update_users()


def update_gui_info(_):
    # 获取选择的用户
    _index = account_list.curselection()

    # 判断是否选择了用户
    if _index:
        _i = users.search(where("uid") == users.all()[_index[0]]["uid"])[0]
        info.config(
            text=f"UID：{_i['uid']}\n电话：{_i['mobile']}\n当前状态：{'cookie有效' if _i['status'] else '请更新cookie'}\n备注：{_i['remarks']}\n添加时间：{time.strftime('%Y年%m月%d日%H时%M分', time.localtime(_i['add_time']))}\n更新时间：{time.strftime('%Y年%m月%d日%H时%M分', time.localtime(_i['update_time']))}")


def get_qr_code():
    global tk_pic
    pic = requests.get(browser.get_login_url()).content
    pic = Image.open(io.BytesIO(pic))
    tk_pic = ImageTk.PhotoImage(pic)
    qrcode_tk.config(image=tk_pic)
    qrcode_tk.pack()
    scan_success.pack()
    # print(update_details())


def get_cookie():
    qrcode_tk.pack_forget()
    cookie = browser.get_cookie()
    if not cookie:
        info.config(text="Cookie 获取失败")
    else:
        if not users.search(where("uid") == cookie[0]):
            users.insert({"uid": cookie[0], "token": cookie[1], "status": True, "add_time": int(time.time()),
                          "update_time": int(time.time()), "remarks": "备注"})
        else:
            users.update({"token": cookie[1], "status": True, "update_time": int(time.time())},
                         where("uid") == cookie[0])

        update_users()
    scan_success.pack_forget()


# 初始化界面
HEIGHT = 620
WIDTH = 620

root = tk.Tk()
root.title("Vipshop Tool")
root.geometry(f"{HEIGHT}x{WIDTH}")
root.minsize(HEIGHT, WIDTH)
root.maxsize(HEIGHT, WIDTH)

# 创建子模块
account = tk.LabelFrame(root, text="ANTONVNKE")
account_op = tk.LabelFrame(account, text="操作")
account_list = tk.Listbox(account)

# 更新用户信息
update_users()

# 挂载
account_list.place(x=10, y=10, width=250, height=HEIGHT - 6 * 10)
account.place(x=10, y=10, width=WIDTH - 2 * 10, height=HEIGHT - 2 * 10)
account_op.place(x=20 + 250, y=0, width=WIDTH - 250 - 6 * 10, height=HEIGHT - 6 * 10)
# 信息
info = tk.Label(account_op, text="选择用户查看信息")
info.pack()

# 操作按钮
tk.Button(account_op, text="更新列表", command=update_users).pack()
tk.Button(account_op, text="导出数据", command=update_orders_excel).pack()
tk.Button(account_op, text="删除", command=delete_user).pack()

# 添加用户
tk.Button(account_op, text="获取登录二维码", command=get_qr_code).pack()
scan_success = tk.Button(account_op, text="我已扫码登录成功", command=get_cookie)
qrcode_tk = tk.Label(account_op, bg='white')

# 列表 bind
account_list.bind("<<ListboxSelect>>", func=update_gui_info)
root.mainloop()
