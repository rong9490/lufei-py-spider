import requests
from lxml import etree
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

url = 'http://www.pearvideo.com/category_5'

page_text = requests.get(url=url, headers=headers).text

parser = etree.HTMLParser(encoding='utf-8')
selector = etree.parse(page_text, parser=parser)
li_list = selector.xpath('//ul[@id="listvideoListUl"]/li')

urls = [] # 所有视频的地址

for li in li_list:
    detail_url = 'https://www.pearvideo.com/' + li.xpath('./div/a/@href')[0]
    name = li.xpath('./div/a/div[2]/text()')[0] + '.mp4'
    detail_page_text = requests.get(url=detail_url, headers=headers).text
    # 解析出视频: xpath不能解析js, 只能用正则
    ex = 'srcUrl="(.*?)",vdoUrl'
    video_url = re.findall(ex, detail_page_text)[0]
    dic = {
        'name': name,
        'url': video_url
    }
    urls.append(dic)

# 阻塞且耗时的操作

from multiprocessing import Pool

def get_video_data(dic):
    url = dic['url']
    data = requests.get(url=url, headers=headers).content
    # 持久化存储也很耗时, 放入pool
    with open(dic['name'], 'wb') as fp:
        fp.write(data)

pool = Pool(4)
pool.map(get_video_data, urls)

pool.close()
pool.join() # 等待子线程