#爬取所有研究生学校信息

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import json


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

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
    school_name = {'研招网': {'website': 'https://yz.chsi.com.cn/', 'info': '', 'into': '', 'select': ''}}

    # for i in range(44):
    #     j = i * 20
    #     get_per_html(school_name,'https://yz.chsi.com.cn/sch/search.do?',str(j))
    #引入多线程线程池 from multiprocessing import Pool
    #教程 https://morvanzhou.github.io/tutorials/python-basic/multiprocessing/5-pool/
    #
    # def multicore():
    #     pool = mp.Pool()
    #     res = pool.map(job, range(10))
    #     print(res)
    #     res = pool.apply_async(job, (2,))
    #     # 用get获得结果
    #     print(res.get())
    #     # 迭代器，i=0时apply一次，i=1时apply一次等等
    #     multi_res = [pool.apply_async(job, (i,)) for i in range(10)]
    #     # 从迭代器中取出
    #     print([res.get() for res in multi_res])

    pool = Pool()
    multiple_results = [pool.apply_async(get_per_html(school_name,'https://yz.chsi.com.cn/sch/search.do?',str(i*20)), (i)) for i in range(44)]
    print(multiple_results)
    #save_json(school_name, 'all_school')