import time

from selenium.webdriver.common.by import By


def get_qr_code(browser):
    browser.get("https://passport.vip.com/login?src=https%3A%2F%2Fwww.vip.com%2F")
    browser.delete_all_cookies()
    browser.get("https://passport.vip.com/login?src=https%3A%2F%2Fwww.vip.com%2F")
    src = browser.find_element(By.CLASS_NAME, "J-qr-img").get_attribute("src")
    # print(src)
    return src


def get_cookie(browser):
    # 循环检测 COOKIE获取 VipRUID PASSPORT_ACCESS_TOKEN
    for _ in range(10):
        if browser.get_cookie("VipRUID") and browser.get_cookie("PASSPORT_ACCESS_TOKEN"):
            return browser.get_cookie("VipRUID")["value"], browser.get_cookie("PASSPORT_ACCESS_TOKEN")["value"]
        else:
            time.sleep(5)


if __name__ == '__main__':
    from utils.get_browser import chrome

    b = chrome()
    print(get_qr_code(b))
    print(get_cookie(b))
