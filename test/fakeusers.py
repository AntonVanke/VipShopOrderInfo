import random
import string
import time


# 生成一个随机的 uid，范围是 100000000 到 999999999
def random_uid():
    return str(random.randint(100000000, 999999999))


# 生成一个随机的 token，长度是 40，由大写字母和数字组成
def random_token():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=40))


# 生成一个随机的 status，值是 True 或 False
def random_status():
    return random.choice([True, False])


# 生成一个随机的 add_time 和 update_time，范围是 2020-01-01 到 2023-12-31，格式是 Unix 时间戳
def random_time():
    start_date = time.mktime((2020, 1, 1, 0, 0, 0, 0, 0, 0))
    end_date = time.mktime((2023, 12, 31, 23, 59, 59, 0, 0, 0))
    delta = end_date - start_date
    random_seconds = random.randrange(delta + 1)
    random_time = start_date + random_seconds
    return int(random_time)


# 生成一个随机的 mobile 和 username，长度是 11，由数字组成，前三位是常见的手机号码段
def random_mobile():
    # 常见的手机号码段有：130-139，150-159，170-179，180-189
    prefix = random.choice(["13", "15", "17", "18"])
    suffix = "".join(random.choices(string.digits, k=8))
    return prefix + suffix


# 隐藏手机号码中间四位数字
def hide_mobile(mobile):
    return mobile[:3] + "****" + mobile[7:]


# 生成一个随机的 remarks，长度是 2 到 10，由汉字组成
def random_remarks():
    # 汉字的 Unicode 范围是 \u4e00 到 \u9fa5
    return "".join(random.choices("\u4e00\u9fa5", k=random.randint(2, 10)))


# 固定 nickname 的值为 "唯品会会员"
def fixed_nickname():
    return "唯品会会员"


# 根据给定的列表长度，生成一个包含假数据的列表
def generate_fake_data(length):
    data = {}
    for i in range(1, length + 1):
        mobile = random_mobile()
    data[str(i)] = {
        "uid": random_uid(),
        "token": random_token(),
        "status": random_status(),
        "add_time": random_time(),
        "update_time": random_time(),
        "mobile": hide_mobile(mobile),
        "username": hide_mobile(mobile),
        "remarks": random_remarks(),
        "nickname": fixed_nickname()
    }

    return data


if __name__ == '__main__':
    # 打印出一个包含10个假数据的列表
    print(generate_fake_data(10))
