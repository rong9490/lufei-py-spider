#!/usr/bin/env python
# -*- coding:utf-8 -*-
#- 需求: 爬取搜狗首页
import requests
print("01.py")
if __name__ == "__main__":
    url = 'https://www.sogou.com/'
    response = requests.get(url=url)
    # NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/302
    page_text = response.text
    print(page_text)
    # 持久化存储
    with open('./sogou.html', 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print('爬取搜狗结束..')

