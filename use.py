import json
import requests
from bs4 import BeautifulSoup

def load_json(file):
    with open(file,'r',encoding='utf-8') as f:
        new_dict = json.load(f)
    return new_dict

if __name__ == '__main__':
    school = load_json("all_school.json")
    school['清华大学']['website'] = ''
    headers ={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36'
    }
    respose = requests.get('https://www.baidu.com/ssid=f0d16d656e67716931323331323330347bc3/from=844b/s?word=清华大学')
    bs = BeautifulSoup(respose.text)
    print(bs)
