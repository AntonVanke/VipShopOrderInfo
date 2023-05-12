import time

from pywebio import start_server
from pywebio.input import input
from pywebio.output import put_text

# 模拟数据库中的用户信息
WEB_ACCESS = "8D8735985D2054ACB4B2F93365DE4124A1F3F3FFE19E6B9C897A40E0EDC6C90D"


def login():
    web_access = input("请输入密钥")

    # 验证用户名和密码是否正确
    if WEB_ACCESS == web_access:
        put_text("登录成功！")
        main()
    else:
        put_text("密钥输入错误！")


def main():
    put_text("你好ZG")


if __name__ == '__main__':
    # 启动 web 服务器
    start_server(login, port=8080, auto_open_webbrowser=True, debug=True)
