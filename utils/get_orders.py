import json
import requests


def get_order(vip_ruid, passport_access_token, page_size=100):
    cookies = {
        'VipRUID': f'{vip_ruid}',
        'PASSPORT_ACCESS_TOKEN': f'{passport_access_token}',
    }
    headers = {
        'referer': 'https://order.vip.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    }

    params = {
        'api_key': '70f71280d5d547b2a7bb370a529aeea1',
        'page_size': f'{page_size}',
    }

    response = requests.get(
        'https://mapi.vip.com/vips-mobile/rest/order/pc/get_union_order_list/v1',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    json.dump(response.json(), open(f"{passport_access_token}.json", "w", encoding="utf-8"), ensure_ascii=False)
