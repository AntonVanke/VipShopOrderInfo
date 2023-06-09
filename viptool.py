import time
from functools import lru_cache

import requests
from logzero import logger, logfile
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By


class VipShopUser:
    def __init__(self, uid, token):
        """
        初始化一个用户
        :param uid: VipRUID
        :param token: PASSPORT_ACCESS_TOKEN
        """
        self.uid = uid
        self.token = token
        self.cookies = {
            'VipRUID': f'{self.uid}',
            'PASSPORT_ACCESS_TOKEN': f'{self.token}',
        }
        self.headers = {
            'referer': 'https://order.vip.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        }

    @lru_cache(None)
    def get_details(self, order_sn):
        """
        获取订单详细信息
        :param order_sn: 订单号
        :return:
        """
        params = {
            'orderClient': 'pc',
            'orderSn': f'{order_sn}',
        }
        response = requests.get('https://order.vip.com/multDetail/order/info', params=params, cookies=self.cookies,
                                headers=self.headers)
        logger.debug(f"{self.uid}获取{order_sn}订单详情")
        return response.json()

    @lru_cache(None)
    def get_orders(self, page_size=100):
        """
        获取订单
        :param page_size: 订单数 max: 100
        :return:
        """
        params = {
            'api_key': '70f71280d5d547b2a7bb370a529aeea1',
            'page_size': f'{page_size}',
        }
        response = requests.get(
            'https://mapi.vip.com/vips-mobile/rest/order/pc/get_union_order_list/v1',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        )
        # 获取订单列表
        logger.debug(f"{self.uid}获取订单列表")
        return response.json()

    @lru_cache(None)
    def user_info(self):
        """
        获取用户信息
        :return:
        """
        logger.debug(f"{self.uid}获取用户信息")
        response = requests.get('https://myi.vip.com/api/account/base_info', cookies=self.cookies, headers=self.headers)
        return response

    @lru_cache(None)
    def is_visible(self):
        """
        判断 cookie 有效性
        :return:
        """
        response = self.user_info()
        try:
            return response.json()["code"] == "200"
        except (requests.exceptions.JSONDecodeError, KeyError):
            return False

    @lru_cache(None)
    def get_user_info(self):
        return self.user_info().json()


class BrowserWeb:
    def __init__(self):
        self.browser_options = EdgeOptions()
        # 不显示调试提示
        self.browser_options.add_experimental_option('useAutomationExtension', False)
        self.browser_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        # 防止报错
        self.browser_options.add_argument('--no-sandbox')
        self.browser_options.add_argument('--disable-dev-shm-usage')
        # 无头模式
        self.browser_options.add_argument('--headless')
        self.browser_options.add_argument('--disable-gpu')
        self.browser = Edge(options=self.browser_options)
        self.browser.get("https://passport.vip.com/")
        logger.debug(f"{self.browser.name}浏览器初始化成功")

    def get_login_url(self):
        """
        获取 二维码
        :return: 图片地址
        """
        self.browser.get("https://passport.vip.com/login?src=https%3A%2F%2Fwww.vip.com%2F")
        self.browser.delete_all_cookies()
        self.browser.get("https://passport.vip.com/login?src=https%3A%2F%2Fwww.vip.com%2F")
        src = self.browser.find_element(By.CLASS_NAME, "J-qr-img").get_attribute("src")
        logger.debug("获取登录二维码成功")
        # return "https://mlogin.vip.com/asserts/login/qrcode.html?" + src.split("?")[1]
        return src

    def get_cookie(self):
        # 循环检测 COOKIE获取 VipRUID PASSPORT_ACCESS_TOKEN
        for _ in range(10):
            try:
                if self.browser.get_cookie("VipRUID") and self.browser.get_cookie("PASSPORT_ACCESS_TOKEN"):
                    logger.warning(f"Cookie获取成功{self.browser.get_cookie('VipRUID')['value']}")
                    return self.browser.get_cookie("VipRUID")["value"], \
                        self.browser.get_cookie("PASSPORT_ACCESS_TOKEN")[
                            "value"]
            except (TypeError, KeyError):
                pass
            finally:
                time.sleep(5)
        logger.warning("Cookie获取失败")
        return False
