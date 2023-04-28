import time
import yaml

from selenium.webdriver.common.by import By
from get_browser import chrome


def get_qr_code():
    browser.get("https://passport.vip.com/login?src=https%3A%2F%2Fwww.vip.com%2F")
    browser.delete_all_cookies()
    browser.get("https://passport.vip.com/login?src=https%3A%2F%2Fwww.vip.com%2F")
    return browser.find_element(By.CLASS_NAME, "J-qr-img").get_attribute("src")


def get_cookie():
    # 循环检测 COOKIE获取 VipRUID PASSPORT_ACCESS_TOKEN
    for _ in range(10):
        if browser.get_cookie("VipRUID") and browser.get_cookie("PASSPORT_ACCESS_TOKEN"):
            return browser.get_cookie("VipRUID")["value"], browser.get_cookie("PASSPORT_ACCESS_TOKEN")["value"]
        else:
            time.sleep(5)


browser = chrome()
if __name__ == '__main__':
    print(get_qr_code())
    print(get_cookie())
