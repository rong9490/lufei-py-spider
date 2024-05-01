import requests
import re
import os

if __name__ == "__main__":
    # 创建文件夹
    if not os.path.exists('./qiutuLibs'):
        os.mkdir('./qiutuLibs')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    # 如何爬取图片: 通用模板 含分页
    url = 'https://www.qiushibaike.com/pic/page/%d/?s=5184961'
    for pageNum in range(1, 36):
        new_url = format(url%pageNum)
        # 通用爬虫
        page_text = requests.get(url=new_url, headers=headers).text
        # 页面内容进行提取
        ex = '<div class="thumb">.*?<img src="(.*?)" alt.*?</div>'
        # 拿到所有的图片地址
        img_src_list = re.findall(ex, page_text, re.S)  # 单行匹配/多行匹配

        for src in img_src_list:
            src = 'https:' + src
            img_data = requests.get(url=src, headers=headers).content  # 二进制数据
            # 取得图片名称
            img_name = src.split('/')[-1]
            img_path = './qiutuLibs/' + img_name
            with open(img_path, 'wb') as fp:
                fp.write(img_data)
                print(img_name, '下载成功')


