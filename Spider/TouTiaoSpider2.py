from urllib.parse import urlencode
import json
import requests
from requests import RequestException
from bs4 import BeautifulSoup

def get_page_index(offset):
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

def parse_page(html):
    data = json.loads(html)
    if data and 'data' in data:
        for item in data.get('data'):
            if item.get('article_url') is not None:
                yield item.get('article_url')


def get_image_detail(url):
    # print('====get_image_detail====')
    # print('url is ' + url)
    try:
        header = {
            'cookie': 'tt_webid=6747853276639249924; s_v_web_id=76f66fe05f4a260add644dda8ed901de; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6747853276639249924; csrftoken=17008ea99e3784ae39bb365373aeb02c; __tasessionId=qney9mtiz1571127593522',
            'host': 'www.toutiao.com',
            'referer': 'https://www.toutiao.com/a6747818977268859400/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.get(url,headers=header)
        if response.status_code == 200:
            html = response.text
            return html
        else:
            print('request abnormal')

    except RequestException:
        print('a get image detail exception occurred')


def parse_image_detail(content):
    # print('====parse detail====')
    soup = BeautifulSoup(content,'lxml')
    title = soup.title.string
    print(title)
    try:
        imgs = soup.find_all('img')
        print(imgs)
    except Exception:
        print("yichang")
    # for img in imgs:
    #     print(img)
    # pgc_imgs = soup.find_all(class_='pgc_img')
    # if pgc_imgs is not None:
    #     for pgc_img in pgc_imgs:
    #         print(pgc_img)
    #         # image_url = pgc_img.find_all('img')['src']
    #         # print(image_url)
    # else:
    #     print("None")


def main():
    html = get_page_index(20)
    urls = parse_page(html)
    for url in urls:
        # print(url)
        content = get_image_detail(url)
        if content is not None:
            parse_image_detail(content)


if __name__ == '__main__':
    main()