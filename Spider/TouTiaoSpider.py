import requests
import re
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
from hashlib import md5
import os
from multiprocessing import Pool

def get_page_index(keyword,offset):
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': 1571118951322
    }
    header = {
        'cookie': '__tasessionId=ampozol5g1563806844189; tt_webid=671649' +
                  '9234256455175; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16c' +
                  '1a26e5e12df-040ada0c1d8081-c343162-100200-16c1a26e5e428c; CNZZDAT' +
                  'A1259612802=945869726-1563806204-https%253A%252F%252Fwww.google.c' +
                  'om%252F%7C1563806204; tt_webid=6716499234256455175; csrftoken=46' +
                  'a41d4141000920aea9354904736a2d; s_v_web_id=2b8f7242614ce9f3dd7cbf' +
                  '26d932530d',
        'host': 'www.toutiao.com',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit' +
                      '/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    url = 'https://www.toutiao.com/api/search/content/?'+urlencode(data)
    try:
        response = requests.get(url,headers=header)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            print("====request successful====")
            return response.text
        else:
            print(response.status_code)
            return None
    except RequestException:
        print('请求发生错误')
        return None


def parse_page_index(html):
    print('====parse page====')
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            title = item.get('title')
            image_list = item.get('image_list')
            if image_list is not None:
                for image in image_list:
                    yield {
                        'title': title,
                        'image': image
                    }
    else:
        print('parse error')


# def get_detail_page(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.text
#         else:
#             return None
#     except RequestException:
#         print('get detail error!!!')
#         return None


# def parse_detail_page(html,url):
#     soup = BeautifulSoup(html,'lxml')
#     result = soup.select('title')
#     title = result[0].get_text() if result else ''
#     pattern = re.compile('gallery:\s+JSON.parse\("(.*?)"\)',re.S)
#     f_result = re.search(pattern,html)
#     print('f_result is ' + str(f_result))

def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image').get('url'))
        if response.status_code == 200:
            filepath = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(filepath):
                with open(filepath,'wb') as f:
                    f.write(response.content)
                    f.close()
    except RequestException:
        print('save Error')


def main(offset):
    html = get_page_index('街拍', offset)
    image_list = parse_page_index(html)
    for item in image_list:
        print(item)
        save_image(item)


if __name__ == '__main__':
    groups = [x*20 for x in range(1,11)]
    pool = Pool()
    pool.map(main,groups)