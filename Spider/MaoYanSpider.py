import requests
import re
from requests.exceptions import RequestException
import json
from multiprocessing import Pool


def get_one_page(url,header):
    try:
        response = requests.get(url,headers=header)
        if response.status_code == 200:
            content = response.text
            pattern = re.compile('<dd>.*?name">.*?href="(.*?)"\s+title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>'
                                 '.*?fraction">(.*?)</i>.*?</dd>',re.S)
            results = re.findall(pattern,content)
            return results
        else:
            print(response.status_code)
            return None
    except RequestException:
        return None


def parse_one_page(results):
    for result in results:
        yield {
            'link': result[0],
            'title': result[1],
            'actor': re.sub('\s','',result[2]),
            'time':result[3],
            'score':result[4]
        }


def main(offset):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
    url = 'https://maoyan.com/board/4?'

    real_url = url + 'offset='+str(offset)
    print(real_url)
    results = get_one_page(real_url,header)
    print(results)
    items = parse_one_page(results)

    for item in items:
        write_to_file(item)


def write_to_file(content):
    with open('E:/maoyan.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    print("==========爬虫程序开始==========")
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
    # for i in range(10):
    #     main(i*10)
    print("==========爬虫程序结束==========")
