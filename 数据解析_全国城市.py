import requests
from lxml import etree

if __name__ == "__main__":
    headers = {}
    url = ""
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    parser = etree.HTMLParser(encoding='utf-8')
    selector = etree.parse(page_text, parser=parser)
    host_li_list = selector.xpath('//div[@class="bottom"]/ul/li')
    all_city_names = []
    for li in host_li_list:
        host_city_name = li.xpath('./a/text()')[0]
        all_city_names.append(host_city_name)
    city_names_list = selector.xpath('//div[@class="bottom"]/ul/div[2]/li')
    for li in city_names_list:
        city_name = li.xpath('./a/text()')[0]
        all_city_names.append(city_name)
    # 优化: 合并两次xpath的选取 用 '或'表达式 |
    len(all_city_names) # 394个