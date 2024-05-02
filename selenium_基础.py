from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver =  webdriver.Chrome()
driver.get('https://www.gushiwen.cn/')
# 查询id为txtKey的节点
txtKey = driver.find_element(By.ID, 'txtKey')
# txtKey = driver.find_element(By.ID, 'txtKeyaa')
print(txtKey)

# 向搜索框中输入内容
txtKey.send_keys('唐诗')
# 查找搜索按钮, 用xpath
search = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/form/input[3]')
search.submit() # 点击提交

# 查找当前所有的超链接
a_list = driver.find_element(By.TAG_NAME, 'a')

# 获取源代码
source = driver.page_source
