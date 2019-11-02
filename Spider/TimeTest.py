import time
from datetime import timedelta
import datetime
import pandas as pd
import json
import jieba
import jieba.analyse

def cut_voca(df,row):
    with open('E:/cut_rng.txt','w',encoding='utf-8') as f:
        for i in range(row):
            seqs = jieba.cut(df['text'][i])
            for seq in seqs:
                f.write(seq + "\n")
        f.close()


if __name__ == '__main__':
    # t = timedelta( - float(2) * 60 * 60)
    # datetime = time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')
    # print(datetime)
    # print((datetime.datetime.now() - timedelta(hours=2)).strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S').format(y='年', m='月', d='日' ,h=':',f=':'))
    df = pd.read_json('E:/weibosearch/rng.json',encoding='utf-8',orient='records')

    count = 0
    row = df.iloc[:,0].size
    print(df['sex'][25] == 'f')
    for i in range(row):
        if df['sex'][i] == 'm':
            count += 1

    print('male count is ' + str(count) )
    print('female count is ' + str(row - count))

    iphone_number = 0
    for i in range(row):
        if df['source'][i].find('iPhone') != -1:
            iphone_number += 1

    print('iphone number is '+str(iphone_number))
    print('iphone percent is ' + str(float(iphone_number/row)))

    HUAWEI_NUMBER = 0
    for i in range(row):
        if df['source'][i].find('HUAWEI') != -1:
            HUAWEI_NUMBER +=1

    print('huawei number is ' + str(HUAWEI_NUMBER))
    print('huawei percent is ' + str(float(HUAWEI_NUMBER / row)))

    # cut_voca(df,row)
    filename = 'E:/cut_rng.txt'
    content = open(filename,'rb').read()
    jieba.analyse.set_stop_words('E:/stopwords.txt')
    tags = jieba.analyse.extract_tags(content,topK=30)
    print(tags)

    for x,w in jieba.analyse.extract_tags(filename,withWeight=True):
        print('%s,%s'%(x,w))


