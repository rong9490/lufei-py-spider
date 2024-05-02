from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver =  webdriver.Chrome()
driver.get('https://www.gushiwen.cn/')

sleep(1)
# 查找我的按钮
mine = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/a[6]')
# 点击我的
mine.click()

# 输入登录信息
email = driver.find_element(By.XPATH, '//*[@id="email"]')
email.send_keys('123456789@qq.com')
pwd = driver.find_element(By.XPATH, '//*[@id="pwd"]')
pwd.send_keys('xxxyyy')
code = driver.find_element(By.XPATH, '//*[@id="code"]')
code.send_keys('1234')
# 找到验证节点, 截取验证码图片
code = driver.find_element(By.ID, 'imgCode').screenshot('code.png')
# 点击登录
driver.find_element(By.XPATH, '//*[@id="denglu"]').submit()

# 如何屏幕滚动? window.scrollTo(0, document.body.scrollHeight)

# 执行js代码
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

# 自动化操作: get / find / send_keys / execute_script / back / forward / close

driver.close()

# 如何拖拽? iframe嵌套无法直接获取定位
# switch_to.frame('frame_id') 需要切换子窗口上下文
# 隔离的子window

# TODO 53集