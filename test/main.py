# VipShopOrderInfo
import csv
import json
import time

HEADER_ORDERS = ["商品编号", "商品名称", "商品型号", "型号数量", "商品价格", "订单号", "用户ID", "订单状态", "订单时间",
                 "订单价格", "爬取时间"]
HEADER_DETAILS = ["订单编号", "订单时间", "订单状态", "用户ID", "订单商品类数", "订单价格", "物流单号", "爬取时间"]


def order_test():
    with open("../data/orders-23042702698216-DBFCAB816A919D044598F2FC7992EFF49A917CAC.json", "r",
              encoding="utf-8") as orders_file:
        orders = json.load(orders_file)
        with open("./test1.csv", "w", encoding="utf-8", newline="") as csv_file:
            cw = csv.writer(csv_file)
            cw.writerow(HEADER_ORDERS)
            for index_order in range(len(orders["data"]["orders"])):
                for index_goods in range(len(orders["data"]["orders"][index_order]["goodsView"])):
                    # 商品编号
                    product_id = orders["data"]["orders"][index_order]["goodsView"][index_goods]["vSkuId"]
                    # 商品名称
                    product_name = orders["data"]["orders"][index_order]["goodsView"][index_goods]["name"]
                    # 商品型号
                    product_size = orders["data"]["orders"][index_order]["goodsView"][index_goods]["sizeName"]
                    # 型号数量
                    product_quantity = orders["data"]["orders"][index_order]["goodsView"][index_goods]["num"]
                    # 商品价格
                    product_price = orders["data"]["orders"][index_order]["goodsView"][index_goods]["price"]
                    # 订单号
                    order_id = orders["data"]["orders"][index_order]["orderSn"]
                    # 用户ID TODO
                    user_id = orders["data"]["orders"][index_order]["orderSn"]
                    # 订单状态
                    order_status = orders["data"]["orders"][index_order]["orderStatusName"]
                    # 订单时间
                    order_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                               time.localtime(orders["data"]["orders"][index_order]["createTime"]))
                    # 订单价格
                    order_amount = orders["data"]["orders"][index_order]["orderAmount"]
                    # 爬取时间
                    crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

                    items = [product_id, product_name, product_size, product_quantity, product_price, order_id, user_id,
                             order_status, order_time, order_amount, crawl_time]
                    cw.writerow(items)


def detail_test():
    with open("../data/details-22-23042702698216.json", "r", encoding="utf-8") as details_file:
        details = json.load(details_file)
        # 订单编号
        order_sn = details["result"]["orderSn"]
        # 订单时间
        order_time = details["result"]["orderTime"]
        # 订单状态
        order_state = details["result"]["orderTrack"]["result"]["currentState"]
        # 用户ID
        user_id = details["result"]["userId"]
        # 订单商品类数
        goods_count = details["result"]["goodsList"]["result"]["goodsTotalCount"]
        # 订单价格
        total_amount = details["result"]["goodsList"]["result"]["totalAmount"]
        # 物流单号
        tracking_sn = details["result"]["orderTrack"]["result"]["orderTrack"][0]["sn"]
        # 爬取时间
        crawl_time = int(time.time())

        items = [order_sn, order_time, order_state, user_id, goods_count, total_amount, tracking_sn, crawl_time]
        with open("./test2.csv", "w", encoding="utf-8", newline="") as csv_file:
            cw = csv.writer(csv_file)
            cw.writerow(HEADER_DETAILS)
            cw.writerow(items)


order_test()
detail_test()
