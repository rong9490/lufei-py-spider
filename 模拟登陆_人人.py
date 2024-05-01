import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
url = 'http://www.renren.com/SysHome.do'
response = requests.get(url=url, headers=headers)
page_text = response.text
parser = etree.HTMLParser(encoding='utf-8')
selector = etree.parse(page_text, parser=parser)
code_img_src = selector.xpath('//*[@id=""verifyPic_login]/@src')[0]
response = requests(url=code_img_src, headers=headers)
code_img_data = response.content
# 持久化存储
with open('./code_verify.jpg', 'wb') as fp:
    fp.write(code_img_data)

# 使用云打码sdk(略)
# 得到最终结果
result = 'xxxyyy'
login_url = 'xx'
data = { 'result': result, 'username': 'xxyy', 'password': 'pwdddddddd' }
response = requests.post(url=login_url, data=data, headers=headers)
login_page_text = response.text
login_page_status_code = response.status_code
print('login_page_status_code', login_page_status_code)
with open('renren.html', 'w', encoding='utf-8') as fp:
    fp.write(login_page_text)

# 如何通用的判断验证, 模拟登录是否成功了 响应状态码 status_code

# 如何在登录后? 的状态: 保存Cookie -> session对象 ->

# 后续的请求发送都通过sesison来进行
session = requests.session()