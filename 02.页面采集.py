import requests

# 反爬机制 与 UA伪装 User-Agent(请求载体)
if __name__ == "__main__":
    # 搜索戴森球 / url序列化
    url = 'https://www.sogou.com/web'
    kw = input('enter a word:')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    param = {
        'query': kw,
    }
    # 携带参数
    response = requests.get(url=url, params=param, headers=headers)

    page_text = response.text
    fileName = kw + '.html'
    with open(fileName, 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print(fileName, '保存成功')
