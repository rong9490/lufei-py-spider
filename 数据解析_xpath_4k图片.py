import requests
import os
from lxml import etree

if __name__ == "__main__":
    url = 'https://bj.58.com/ershoufang/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'  # 解决中文乱码
    page_text = response.text
    parser = etree.HTMLParser(encoding='utf-8')
    selector = etree.parse(page_text, parser=parser)

    # 解析src的属性值 + alt
    li_list = selector.xpath('//div[@class="slist"]/ul/li')
    if not os.path.exists('./picLibs'):
        os.mkdir('./picLibs')
    for li in li_list:
        # 加上这个点. 表示是子作用域，而非全局
        img_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0]
        img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        # 局部设置编码
        img_name = img_name.encode('iso-8859-1').decode('gbk')
        img_data = requests.get(url=img_src, headers=headers).content
        img_path = './picLibs/' + img_name
        with open(img_path, 'wb') as fp:
            fp.write(img_data)