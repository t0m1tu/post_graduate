#爬取所有研究生学校名称

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import sqlite3
import os
import json


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

def get_url(ssdm='',is_985='',is_211='',is_yjsy='',zhx=''):
    uri = "https://yz.chsi.com.cn"
    url = uri + '/sch/search.do?' + 'ssdm=' + ssdm + '&985=' + is_985 + '&211=' + is_211 + '&yjsy'+ is_yjsy + '&zhx=' + zhx
    return url

def get_per_html(school_name,uri='https://yz.chsi.com.cn/sch/search.do?', start_url_number='0'):
    #school_name = {'研招网': {'website': 'https://yz.chsi.com.cn/', 'info': '', 'into': '', 'select': ''}}
    j = 0
    url = uri + "start=" + start_url_number
    respose = requests.get(url)
    bs = BeautifulSoup(respose.text, 'lxml')

    # for tag in bs.find_all("tbody"):
    #     for i in tag.find_all('a'):
    #         if j % 3 == 0:
    #             info = 'https://yz.chsi.com.cn' + i['href']
    #             na = i.text
    #             nam = na.replace('\r\n', '')
    #             name = nam.replace(' ', '')
    #         elif j % 3 == 1:
    #             into = 'https://yz.chsi.com.cn' + i['href']
    #         elif j % 3 == 2:
    #             select = 'https://yz.chsi.com.cn' +  i['href']
    #             school_name[name] = {'info': info, 'into': into, 'select': select}
    #         j = j + 1
    # 上面是之前的，现在改成下面的了

    for tag in bs.find_all("tbody"):
        for i in tag.find_all('td'):
            t = i.text.replace('\n', '')
            te = t.replace('\r', '')
            tex = te.replace(' ', '')
            text = tex.replace('\u2002','/')
            if j % 8 == 0:
                name = text
                info = 'https://yz.chsi.com.cn' + i.a['href']
            if j % 8 == 1:
                location = text
            elif j % 8 == 2:
                belong = text
            elif j % 8 == 3:
                zd = text
            elif j % 8 == 6:
                into = 'https://yz.chsi.com.cn' + i.a['href']
            elif j % 8 == 7:
                select = 'https://yz.chsi.com.cn' + i.a['href']
                school_name[name] = {'info': info, '城市': location, 'is_92': zd, '上属':belong,'into': into, 'select': select}
            j = j + 1
    return school_name

def all_school():
    school_name = {'研招网': {'website': 'https://yz.chsi.com.cn/', 'info': '', 'into': '', 'select': ''}}

    for i in range(44):
        j = i * 20
        get_per_html(school_name,'https://yz.chsi.com.cn/sch/search.do?',str(j))

    save_json(school_name, 'all_school')

def ssdm():
    url = "https://yz.chsi.com.cn/sch/"
    respose = requests.get(url)
    bs = BeautifulSoup(respose.content, "lxml")
    ssdm = {}
    for tag in bs.find_all(id='ssdm'):
        for i in tag.find_all(value=True):
            key = i.attrs['value']
            val = i.text
            valu = val.replace('\r\n', '')
            value = valu.replace(' ','')
            ssdm[key] = value
    return ssdm

def save_db(data):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.close()
    conn.commit()
    conn.close()

def save_txt(data,name):
    data = json.dumps(data)
    with open(name + '.txt', 'w', encoding='utf-8') as f:
        f.write(data)

#写入字典，需要用json.dump,中文加入ensure_ascii=False
def save_json(data,name):
    with open( name + '.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f,ensure_ascii=False)

def load_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        print(f.read())
        return f.read()

def load_json(file):
    with open(file,'r',encoding='utf-8') as f:
        new_dict = json.load(f)
    return new_dict

if __name__ == '__main__':
    all_school()
    #load_json("all_school.json")