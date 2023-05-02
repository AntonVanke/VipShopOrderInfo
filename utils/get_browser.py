from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.chrome.webdriver import Service


def chrome():
    browser_options = ChromeOptions()
    # Service(executable_path="./chromedriver")
    # 不显示调试提示
    browser_options.add_experimental_option('useAutomationExtension', False)
    browser_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    # 防止报错
    browser_options.add_argument('--no-sandbox')
    browser_options.add_argument('--disable-dev-shm-usage')
    # browser_options.add_argument('--headless')
    # browser_options.add_argument('--disable-gpu')
    # browser_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 9; FKU-SB00) AppleWebKit/537.36 (KHTML, "
    #                              "like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 EdgA/109.0.1518.53")
    # browser_options.add_argument(r"--user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data")

    browser = Chrome(options=browser_options)

    # 设置检测规避
    # stealth_js = open("./stealth.min.js", "r").read()
    # browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': stealth_js})
    browser.get("https://passport.vip.com/")
    return browser
