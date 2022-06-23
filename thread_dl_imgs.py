import re
import time
import random
from concurrent.futures import ThreadPoolExecutor
from urllib import parse

import requests


def get_img(img_info: tuple):
    img_url, img_name = img_info
    url, name_ = parse.unquote(img_url).replace('/200', '/0'), parse.unquote(img_name)
    try:
        img = requests.get(url=url, headers=headers).content
        with open(f'./王者荣耀壁纸/{name_}.jpg', 'wb') as wf:
            wf.write(img)
        print(f'{name_}下载成功！')
    except Exception:
        print(f'********{name_} 下载失败！！！*********')
        fail_li.apend(url)


def get_html_info(page):
    url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi'
    time_stamp = int(time.time() * 1000)
    pay_load = {
        "activityId": "2735",
        "sVerifyCode": "ABCD",
        "sDataType": "JSON",
        "iListNum": "20",
        "totalpage": "0",
        "page": page,
        "iOrder": "0",
        "iSortNumClose": "1",
        "jsoncallback": f"jQuery17106664578181835136_165595692{random.randint(1000, 9999)}",
        "iAMSActivityId": "51991",
        "_everyRead": "true",
        "iTypeId": "2",
        "iFlowId": "267733",
        "iActId": "2735",
        "iModuleId": "2735",
        "_": str(time_stamp)
    }
    text_page = requests.get(url=url, params=pay_load, headers=headers).text
    result_url = re.findall(r'sProdImgNo_6":"(.*?)","sProdImgNo_7".*?"sProdName":"(.*?)","', text_page, re.S)
    print(f"获取第{page + 1}页图片信息成功！")
    with ThreadPoolExecutor(max_workers=20) as down_pool:
        down_pool.map(get_img, result_url)


def thread_pool():
    page_list = list(range(30))
    with ThreadPoolExecutor(max_workers=8) as pool:
        pool.map(get_html_info, page_list)


if __name__ == '__main__':
    headers = {
        'User-Agnet': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    fail_li = []
    thread_pool()
    print('\nDone\n')
    print(f'download fail list:\n{fail_li}')
