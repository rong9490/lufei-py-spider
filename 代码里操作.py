import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

url = 'https://www.baidu.com/s?wd=ip'

response = requests.get(url=url, headers=headers, proxies={'https': '222.110.147.50:3128'})
page_text = response.text

with open('ip.html', 'w', encoding='utf-8') as fp:
    fp.write(page_text)