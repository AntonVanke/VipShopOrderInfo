import csv
import time
import tkinter as tk

from tinydb import TinyDB, where, Query

from viptool import VipShopUser, BrowserWeb

# TODO: 初始化浏览器
# browser = BrowserWeb()

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


def update_users():
    for _user in users.all():
        if VipShopUser(uid=_user["uid"], token=_user["token"]).is_visible():
            users.update({"status": True}, where("uid") == _user["uid"])
        else:
            users.update({"status": False}, where("uid") == _user["uid"])

    for _user in users.search(where("status") == True):
        user_info = VipShopUser(uid=_user["uid"], token=_user["token"]).get_user_info()["data"]
        users.update(
            {"mobile": user_info["mobile"], "username": user_info["userName"], "nickname": user_info["nickname"]},
            where("uid") == _user["uid"])
    account_list.delete(0, tk.END)

    # 筛洗出有效信息
    for user in users.all():
        user_nsi = {k: v for k, v in user.items() if k in ["username", "remarks", "status", "nickname"]}

        account_list.insert(tk.END,
                            f'{user_nsi["username"]}-{user_nsi["remarks"]}-{"有效" if user_nsi["status"] else "失效"}-{user_nsi["nickname"]}')

    return True


# 初始化界面
HEIGHT = 620
WIDTH = 620

root = tk.Tk()
root.title("Vipshop Tool")
root.geometry(f"{HEIGHT}x{WIDTH}")
root.minsize(HEIGHT, WIDTH)
root.maxsize(HEIGHT, WIDTH)

# 创建 账户 子模块
account = tk.LabelFrame(root, text="账号管理")
account_list = tk.Listbox(account)

# 更新用户信息
update_users()

# 挂载
account_list.place(x=10, y=10, width=250, height=200 - 4 * 10)
account.place(x=10, y=10, width=WIDTH - 2 * 10, height=200)


def test():
    data = update_orders()
    with open("data.csv", "w", encoding="gbk", newline="") as f:
        # 创建csv写入对象
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        # 写入表头
        writer.writeheader()
        # 写入数据
        writer.writerows(data)
    import os
    os.system("start excel data.csv")


tk.Button(account, text="更新列表", command=update_users).pack()
tk.Button(account, text="导出数据", command=test).pack()
root.mainloop()
