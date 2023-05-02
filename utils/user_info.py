import requests


def user_info(vip_ruid, passport_access_token):
    cookies = {
        'VipRUID': f'{vip_ruid}',
        'PASSPORT_ACCESS_TOKEN': f'{passport_access_token}',
    }
    headers = {
        'referer': 'https://order.vip.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    }

    response = requests.get('https://myi.vip.com/api/account/base_info', cookies=cookies, headers=headers)
    return response


def is_visible(vip_ruid, passport_access_token):
    response = user_info(vip_ruid, passport_access_token)
    try:
        return response.json()["code"] == "200"
    except (requests.exceptions.JSONDecodeError, KeyError):
        return False


def get_user_info(vip_ruid, passport_access_token):
    return user_info(vip_ruid, passport_access_token).json()
