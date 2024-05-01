# pip3 install bs4
# pin3 install lxml

from bs4 import BeautifulSoup
import requests

# 本地页面调试 soup.html
if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    url = 'https://so.gushiwen.cn/mingju/juv_b9ebe90d7cf0.aspx'
    page_text = requests.get(url=url, headers=headers)
    # print(page_text.content)
    soup = BeautifulSoup(page_text.content, 'lxml')
    # title_div = soup.find('#sonsyuanwen')
    # print(title_div.string)

    fp = open('./sanguo.txt', 'w', encoding='utf-8')
    li_list = soup.select('.book-mulu > ul > li')
    for li in li_list:
        title = li.a.string
        detail_url = 'http://www.shicimingju.com' + li.a['href']
        detail_page_text = requests.get(url=detail_url, headers=headers).text
        # 解析详情内容
        detail_soup = BeautifulSoup(detail_page_text, 'lxml')
        div_tag = detail_soup.find('div', class_='chapter_content')
        # 章节: 标题 + 内容 + 换行
        content = div_tag.text
        fp.write(title + ':' + content + '\n')

