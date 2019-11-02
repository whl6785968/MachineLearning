import requests
from requests.exceptions import RequestException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import pandas as pd
import re


chromedriver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
#开启开发者模式，防止网站检查出自动控制的存在
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
wait = WebDriverWait(browser,10)
number = 1

def search():
    print('========自动测试========')
    try:
        browser.get('http://218.94.78.75:20001/sjzx/')
        wq = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainmenuItem_1')))
        if wq:
            wq.click()

        enlarge = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#navigator_0 > img:nth-child(1)')))
        enlarge.click()

        html = browser.page_source

        return html
        #
        # images = doc.find('#graphicsLayer4_layer image')
        # for image in images:
        #     # print(lxml.html.tostring(image))
        #     water_quality = str(image.get('xlink:href'))
        #     result = re.match('.*?(\d+).*?',water_quality)
        #
        #     if result is None:
        #         water_quality = '未知'
        #     else:
        #         water_quality = result.group(1)
        #
        #     x = image.get('x')
        #     y = image.get('y')
        #
        #     water_image_info = [[water_quality,x,y]]
        #     print(water_image_info)

    except TimeoutError:
        print('Timeout')

def parse_page(html):
    print('========解析数据========')
    pattern = re.compile('<div\s+.*?id="waterstationItem_\d+".*?<div\s+class="listitem.*?150px;">(.*?)</div><div\s+class="listitem.*?80px;">(.*?)</div></div>')
    results = re.findall(pattern,html)
    for result in results:
        station_name,water_quality = result
        if water_quality == '':
            water_quality = '未知'
        water_info = [[station_name,water_quality]]
        save_to_csv(water_info)


def save_to_csv(water_info):
    print('========保存数据========'+str(water_info))
    global number
    filename = "E:/waterInfo.csv"
    if number == 1:
        csv_headers = ['station_name','water_quality']
        data = pd.DataFrame(water_info)
        data.to_csv(filename,header=csv_headers,index=False,mode='a+',encoding='utf-8',sep=',')
        number += 1
    else:
        data = pd.DataFrame(water_info)
        data.to_csv(filename, index=False, header=False, mode='a+', encoding='utf-8', sep=',')
        number = number + 1

def main():
    print('========爬取开始========')
    html = search()
    parse_page(html)
    print('========爬取结束========')

if __name__ == '__main__':
    main()