# -*- coding: utf-8 -*-
import re
import requests
from concurrent.futures import ThreadPoolExecutor


def download_imgs(img_info: tuple):
    url = f'https:{img_info[0]}'
    img_name = img_info[1]
    try:
        img = requests.get(url=url).content
        with open(f'./CFM壁纸/{img_name}.jpg', 'wb') as wf:
            wf.write(img)
        print(f'{img_name}下载成功！')
    except Exception:
        fail_url.append((url, img_name))


def main(page):
    tg_url = 'https://apps.game.qq.com/wmp/v3.1/'
    pay_load = {
        "p0": "34",
        "p1": "searchNewsKeywordsList",
        "page": page,
        "pagesize": "15",
        "order": "sIdxTime",
        "r0": "script",
        "r1": "NewsObj6473677618485585",
        "type": "iType",
        "id": "1415",
        "source": ""
    }
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Referer': 'https://cfm.qq.com/'
    }
    imgs_info = requests.get(url=tg_url, params=pay_load, headers=headers).text
    res = re.findall(r'"url":"(.*?)","urlCI.*?"sTitle":"(.*?)","sUrl"', imgs_info, re.S)
    with ThreadPoolExecutor(max_workers=len(res)) as pool:
        pool.map(download_imgs, res)


if __name__ == '__main__':
    fail_url = []
    for i in range(1, 4):
        main(i)

    print("\nDownload completed!")
    if fail_url:
        print(f'\n下载失败url:\n{fail_url}')
