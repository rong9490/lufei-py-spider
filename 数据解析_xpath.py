# pip3 install lxml
# xpath 原理: 实例化etree / xpath表达式 / etree.parse / 内容捕获

from lxml import etree
if __name__ == "__main__":
    parser = etree.HTMLParser(encoding='utf-8')
    selector = etree.parse('./soup.html', parser=parser)
    # result = etree.tostring(selector)
    # / 与 // 的区别
    # div[@class="song"]
    # div[@class="song"]/p[3] (索引定位, 从1开始的)
    # "//div[@class="tang"]//li[5]/a/text()"[0] 标签中直系文本
    # "//li[7]//text()" 间隔的非直系的文本
    # "//div[@class="tang"]//text()" 所有的文本内容
    result_list = selector.xpath('/html/head/title')
    result = result_list[0].text
    print(result)