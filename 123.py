import requests
from requests.exceptions import RequestException    
import re
import json
from pyecharts import Pie

def get_one_page(url):
    try:
        user_angent='User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        headers={"User-Agent":user_angent}
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern=re.compile(r'<dd>.*?board-index-.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">\s*?(.*?)\s*?</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time' :item[4].strip()[5:],
            'score':item[5]+item[6]
        }

def parse_country(html):
    pattern=re.compile(r'releasetime">.*?\d+-\d+-\d+\((.*?)\)</p>')
    items=re.findall(pattern,html)
    return items;

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
    
def generate_pie(li1):
    li2=list(set(li1));
    v1=list({})
    length=len(li2)
    for index in range(0,len(li2),1):
        v1.append(li1.count(li2[index]))

    pie =Pie("国家占比")
    pie.add("国家", li2, v1, is_label_show=True)
    pie.render()
    


def main():
    url='http://maoyan.com/board/4?'
    li1=list({})
    for offset in range(0,100,10):
        print(offset)
        full_url=url+'offset='+str(offset)    
        html=get_one_page(full_url)
        for it in parse_one_page(html):
            write_to_file(it)
        li1+=parse_country(html)
    generate_pie(li1)
    
    


if __name__ == '__main__':
    main()
    
    
