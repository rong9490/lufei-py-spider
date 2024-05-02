# 单线程 + 异步协程

import asyncio

async def request(url):
    print('请求', url)
    return url

# async 函数 执行后返回协程对象

coro = request('www.baidu.com')

# # 创建事件循环对象
# loop = asyncio.get_event_loop()

# # 协程对象注册到loop, 然后启动loop
# loop.run_until_complete(coro)

# task 创建使用
# loop = asyncio.get_event_loop()
# task = loop.create_task(coro)
# print(task) # pending

# loop.run_until_complete(task)
# print(task) # finished

# future
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coro)
print(task) # pending
loop.run_until_complete(task)
print(task) # finished

# 绑定回调
def callback_func(task):
    print(task.result()) # 这里的 result() 返回的是写成对象函数的 return 值

task.add_done_callback(callback_func) # 绑定回调函数, 默认传参: task自身