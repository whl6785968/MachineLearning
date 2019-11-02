import requests
import json

if __name__ == '__main__':
    # try:
    #     response = requests.get('http://api.xiaoxiangdaili.com/app/shortProxy/getIp?appKey=501939677910421504&appSecret=krjeLjHB&cnt=&wt=json%20HTTP/1.1')
    #     print(response.status_code)
    #     print(response.request)
    #     print(response.text)
    #
    #     # jsonString = json.loads(response.text)
    #     # objs = jsonString['obj']
    #     # for obj in objs:
    #     #     print(obj['ip'])
    #
    # except Exception:
    #     print('error')
    print('https://weixin.sogou.com/antispider/?from=%2fweixin%3Fquery%3d%E5%8D%97%E4%BA%AC%26type%3d2%26page%3d6'.find('antispider'))