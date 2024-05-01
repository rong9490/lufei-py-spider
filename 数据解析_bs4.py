# pip3 install bs4
# pin3 install lxml

from bs4 import BeautifulSoup

# 本地页面调试 soup.html
if __name__ == '__main__':
    # 文件描述符
    fp = open('./soup.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'lxml')
    # soup.tagName / soup.find('div')
    # soup.find_all(''tagName)
    # soup.select('.tang > div > ul > a')
    # soup.text / string / get_text() 获取标签所有的标签文本(非直系的文本, 隔层的)
    # soup.select('.tang > ul a')[0]['href']
    print(soup.find('a', class_='left-entry__title'))
