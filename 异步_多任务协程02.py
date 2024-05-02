import asyncio
import time

async def request(url):
    print("开始下载", url)
    # 异步协程中 出现了同步模块的代码, 无法实现异步! 降级了
    # time.sleep(2)

    # 异步阻塞操作, 必须手动挂起
    await asyncio.sleep(3)
    print("结束下载", url)

urls = [
    'www.baidu.com',
    'www.sogou.com',
    'www.bilibili.com',
]

start = time.time()

# 任务列表
tasks = []

for url in urls:
    coro = request(url)
    task = asyncio.ensure_future(coro) # 任务对象
    tasks.append(task)

# 新增任务循环
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks)) # 不能直接传入, 需要wait包一层

end = time.time()

print('time:', end - start)

import aiohttp
# requests.get() 同步请求; 需要升级为异步请求!! 否则会降级为同步
async def get_page(url):
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
          page_text = await response.text()  # 别忽略了这个await, 否则拿不到结果
          print(page_text)

# headers, params/data, proxy='http://ip:port'
