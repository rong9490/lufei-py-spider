import requests

if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    # 如何爬取图片
    url = 'https://image.gcores.com/efe9e0a1263db987d1636e773fd343d5-425-425.png?x-oss-process=image/quality,q_90/format,webp'
    img_data = requests.get(url=url, headers=headers).content
    with open('./gcores.webp', 'wb') as fp:
        fp.write(img_data)