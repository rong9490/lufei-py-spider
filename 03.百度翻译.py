import requests
import json

if __name__ == "__main__":
    post_url = 'https://fanyi.baidu.com/sug'
    word = input('enter a word:')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    data = {
        'kw': word
    }
    response = requests.post(url=post_url, data=data, headers=headers)
    data_json = response.json()  # 返回是json对象
    # print(page_json)
    fileName = word + '.json'
    fp = open(fileName, 'w', encoding='utf-8')
    json.dump(data_json, fp=fp, ensure_ascii=False)
