import requests
from lxml import etree

if __name__ == "__main__":
    url = 'https://bj.58.com/ershoufang/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    parser = etree.HTMLParser(encoding='utf-8')
    selector = etree.parse(page_text, parser=parser)
    li_list = selector.xpath('//ul[@class="house-list-wrap"]/li')
    fp = open('58.txt', 'w', encoding='utf-8')
    for li in li_list:
        # 加上这个点. 表示是子作用域，而非全局
        title = li.xpath('./div[2]/h2/a/text()')
        fp.write(title + '\n')