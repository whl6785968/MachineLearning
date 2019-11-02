from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import re
import json


def main():
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        response = requests.get('https://www.toutiao.com/a6747818977268859400/',headers = header)
        if response.status_code == 200:
            html = response.text
            pattern = re.compile('gallery:\s+JSON.parse\("(.*?)"\)',re.S)
            content = re.search(pattern,html)
            result = json.loads(content.groups(1)[0].replace('\\',''))
            print(result)
            # sub_images = result.sub_images
            if result and 'sub_images' in result.keys():
                sub_images = result.get('sub_images')
                images = [item.get('url').replace('u002F','/') for item in sub_images ]
                print(str(images))
    except RequestException:
        print("error")

if __name__ == '__main__':
    main()