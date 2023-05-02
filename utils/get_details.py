import requests
import json


def get_details(vip_ruid, passport_access_token, order_sn):
    cookies = {
        'VipRUID': f'{vip_ruid}',
        'PASSPORT_ACCESS_TOKEN': f'{passport_access_token}',
    }

    headers = {
        'referer': 'https://order.vip.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    }

    params = {
        'orderClient': 'pc',
        'orderSn': f'{order_sn}',
    }

    response = requests.get('https://order.vip.com/multDetail/order/info', params=params, cookies=cookies,
                            headers=headers)
    details = response.json()
    return details
    # json.dump(details, open(f"data/details-{details['result']['status']}-{order_sn}.json", "w", encoding="utf-8"), ensure_ascii=False)
