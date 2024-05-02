import time

# 单线程串行

def get_page(url):
    print("开始下载--", url)
    time.sleep(2)
    print("--结束下载", url)

name_list = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff']

start_time = time.time()

for i in range(len(name_list)):
    get_page(name_list[i])

end_time = time.time()
print('%d 最终完成'% (end_time - start_time))


# 线程池: 阻塞并耗时的操作

from multiprocessing.dummy import Pool

start_time = time.time()
# 实例化线程池实例
pool = Pool(4)
# 传递
pool.map(get_page, name_list)

end_time = time.time()

print('%d 最终完成plus'% (end_time - start_time))