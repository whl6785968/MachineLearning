from urllib.parse import urlencode
import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import json
import time

baseUrl = 'https://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'SUID=6A6F65702013940A000000005B397DB9; usid=jNcKkVDSPAbv_5gU; SUV=00A827C070656F6A5B397DBFD6CD1806; pgv_pvi=4487322624; GOTO=; ssuid=7215005160; _ga=GA1.2.1818826734.1535331204; toutiao_city_news=%E5%8C%97%E4%BA%AC; wuid=AAH+6uYjKAAAAAqLFBvUkggAjQU=; QIDIANID=A4jkGfOpa/iXl+LhXvmV8ESI2AydHIUun9MtAdmv2+PSBlCv6Gcf/lLQre2denSx; IPLOC=CN3201; CXID=C57C7A495FD41B4F2699F4225C615EB1; UM_distinctid=16cb8338218621-0e1e53f1ef4e26-34594872-144000-16cb8338219318; ad=NkUkllllll2NutxjlllllVLPLvyllllltxXKNyllllGlllllRllll5@@@@@@@@@@; ABTEST=7|1571211880|v1; weixinIndexVisited=1; ppinf=5|1571211945|1572421545|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlODclODklRTklOUUlOEJ8Y3J0OjEwOjE1NzEyMTE5NDV8cmVmbmljazoxODolRTUlODclODklRTklOUUlOEJ8dXNlcmlkOjQ0Om85dDJsdUJVaFBQTklfZndsYXNzaGFjUWc3c0FAd2VpeGluLnNvaHUuY29tfA; pprdig=J18QlQ4_-Ulm3-ykhb6tJo5_aRQ2MPUjoB_AFXAi9z9kTkFTn0RWYV4-CkURNBJMXTeidVCOIKpZrHmTw0GmTIirhjDozYTGbWO47h2qkVzNLhNv3LvqehffRTrVi67nvSK_GmzFajQq_GXv2LNDCXkdSKogk6QDlpR2dzmmLT4; sgid=20-43774071-AV2myqm7tqNsghPY3tFPAE4; ld=Xyllllllll2tNfJrlllllVLXmHwlllllLMB6pZllll9lllll9ylll5@@@@@@@@@@; LSTMV=588%2C292; LCLKINT=7792; ppmdig=15712749260000004095b7fcf246ae897949f948881fd98e; JSESSIONID=aaaIrOMTR56Q24fcBAz1w; PHPSESSID=vcj4svmv53sakbsblqdhgjh1o0; SNUID=0066EB398C88189C7A17D77F8D5FF6C9; sct=40',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://weixin.sogou.com/weixin?query=%E5%8D%97%E4%BA%AC&_sug_type_=&sut=1218&lkt=1%2C1571211903597%2C1571211903597&s_from=input&_sug_=y&type=2&sst0=1571211903699&page=21&ie=utf8&w=01019900&dr=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400',
    'X-Requested-With': 'XMLHttpRequest'
}
proxy = None
proxy_list = []
# proxy_pool_url = 'http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=74196d2b43370f85a8f9082737bae6e4&orderNo=GL20191017093223G9tDnWE5&count=10&isTxt=0&proxyType=1'
proxy_pool_url = 'http://api.xiaoxiangdaili.com/app/shortProxy/getIp?appKey=501939677910421504&appSecret=krjeLjHB&cnt=&wt=json%20HTTP/1.1'
max_tried = 5

count_of_proxy = 0

def get_proxy():
    try:
        global count_of_proxy
        print('the count of request proxy is '+str(count_of_proxy))
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            count_of_proxy += 1
            jsonString = json.loads(response.text)
            print(jsonString)
            if jsonString['success'] == False:
                print('sleep 10 seconds')
                time.sleep(10)
                return get_proxy()
            data = jsonString['data'][0]

            return str(data['ip'])+':'+str(data['port'])
            # for obj in objs:
            #     ip = obj['ip']
            #     port = obj['port']
            #     url = str(ip) + ':' +str(port)
            #     proxy_list.append(url)
        else:
            print('error occurred')
            return None
    except RequestException:
        print('request error')
def get_html(url,count=1):
    print('Crawling',url)
    print('The count of tried',count)
    if count>max_tried:
        return None
    global proxy
    try:
        if proxy:
            proxies = {
                'http':'http://'+proxy
            }
            print('use proxy proxy is ' + str(proxies))
            response = requests.get(url,headers=headers,proxies=proxies)
            print('response url is ' + response.url)
        else:
            print('No Proxy')
            response = requests.get(url, headers=headers)
            print('response url is '+response.url)
        if str(response.url).find('antispider') == -1:
            print('Successful Get')
            return response.text
        else:
            print('301')
            proxy = get_proxy()
            if proxy:
                print('Using proxy',proxy)
                return get_html(url)
            else:
                print('get proxy failed')
                return None
    except RequestException as e:
        print('Error Occurred',e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url,count)


def get_index(keyword,page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    url = baseUrl + urlencode(data)
    html = get_html(url)
    return html


def parse_html(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .img-box a').items()
    for item in items:
        article_url = 'https://weixin.sogou.com'+item.attr('href')
        print(article_url)


def main():
    for i in range(1,101):
        html = get_index('南京',i)
        if html:
            parse_html(html)

if __name__ == '__main__':
    main()