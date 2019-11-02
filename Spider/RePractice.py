import re
import requests

if __name__ == '__main__':
    content = requests.get("https://book.douban.com/").text
    pattern = re.compile('<li.*?cover.*?href="(.*?)"\s+title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>',re.S)

    results = re.findall(pattern,content)
    for result in results:
        url,name,author,date = result
        name = re.sub("\s",'',name)
        author = re.sub('\s','',author)
        date = re.sub('\s','',date)
        print(name + ',' + author + ',' + date + ',' + url)
    # print(results)
    # html = '''<div id="songs-list">
    #     <h2 class="title">经典老歌</h2>
    #     <p class="introduction">
    #         经典老歌列表
    #     </p>
    #     <ul id="list" class="list-group">
    #         <li data-view="2">一路上有你</li>
    #         <li data-view="7">
    #             <a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
    #         </li>
    #         <li data-view="4" class="active">
    #             <a href="/3.mp3" singer="齐秦">往事随风</a>
    #         </li>
    #         <li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
    #         <li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
    #         <li data-view="5">
    #             <a href="/6.mp3" singer="邓丽君">但愿人长久</a>
    #         </li>
    #     </ul>
    # </div>'''
    # results = re.findall('<li.*?>\s*?(<a.*?>)?(\w+)(</a>)?\s*?</li>', html, re.S)
    # print(results)
    # for result in results:
    #     print(result[1])