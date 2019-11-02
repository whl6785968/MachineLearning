from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import re
from pyquery import PyQuery as pq
import csv
import codecs
import pandas as pd


chromedriver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
#开启开发者模式，防止网站检查出自动控制的存在
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
#不加载图片
options.add_experimental_option('prefs',{"profile.managed_default_content_settings.images": 2})
browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
wait = WebDriverWait(browser,10)
number = 1

def search():
    print('=====开始搜索=====')
    try:
        browser.get('https://login.taobao.com/member/login.jhtml')
        pwd_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')))
        pwd_login.click()
        weibo_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_OtherLogin > a.weibo-login')))
        weibo_login.click()
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pl_login_logged > div > div:nth-child(2) > div > input')))
        username.send_keys('18245803818')
        pwd = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pl_login_logged > div > div:nth-child(3) > div > input')))
        pwd.send_keys('whl6785968')
        login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#pl_login_logged > div > div:nth-child(7) > div:nth-child(1) > a > span')))
        login.click()
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q'))
        )

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食')
        submit.click()

        # scroll_js = 'window.scrollTo(0,document.body.scrollHeight)'
        # browser.execute_script(scroll_js)
        #检查当前input中的数字与高亮的数字是否为同一个数字
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_data()
        return total.text
    except TimeoutError:
        return search()


def next_page(page_number):
    print('=====跳转下一页=====')
    try:
        page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        page.clear()
        page.send_keys(page_number)
        next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        next.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_data()
    except TimeoutError:
        return next_page(page_number)

def get_data():
    print('=====获取数据=====')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        image = 'https:'+str(item.find('.pic .img').attr('src'))
        price = item.find('.price').text()
        deal_cnt = item.find('.deal-cnt').text()[:-3]
        title = item.find('.title').text()
        shopname = item.find('.shopname').text()
        location  = item.find('.location').text()
        product = [[image,price,deal_cnt,title,shopname,location]]
        # product = {
        #     'image': 'https:' + str(item.find('.pic .img').attr('src')),
        #     'price': item.find('.price').text(),
        #     'deal_cnt': item.find('.deal-cnt').text()[:-3],
        #     'title': item.find('.title').text(),
        #     'shopname': item.find('.shopname').text(),
        #     'location': item.find('.location').text(),
        # }
        print(product)
        save_to_csv(product)

def save_to_csv(product):
    print('=====存储数据=====')
    filename = 'E:/taobao.csv'
    global number
    # with codecs.open(filename,'a','utf-8') as f:
    #     if number == 1:
    #         header = ['image','price','deal_cnt','title','shopname','location']
    #         writer = csv.DictWriter(f,fieldnames=header)
    #         writer.writeheader()
    #     else
    #         try:
    #             writer.writerow(product)
    #         except UnicodeEncodeError:
    #             print('编码错误')
    if number == 1:
        print('number == 1 execute')
        csv_headers = ['image','price','deal_cnt','title','shopname','location']
        data = pd.DataFrame(product)
        data.to_csv(filename,header=csv_headers,index=False,mode='a+',encoding='utf-8',sep=',')

        number = number + 1
    else:
        data = pd.DataFrame(product)
        data.to_csv(filename, index=False,header=False, mode='a+', encoding='utf-8',sep=',')
        number = number + 1

def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    finally:
        browser.close()


if __name__ == '__main__':
    main()
