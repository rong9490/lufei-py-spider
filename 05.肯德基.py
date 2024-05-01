import requests
import json

if __name__ == "__main__":
    url = "https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    data = {
        'cname': '',
        'pid': '',
        'keyword': '番禺',
        'pageIndex': '1',
        'pageSize': '10',
    }
    response = requests.post(url=url, data=data, headers=headers)
    list_data = response.json()
    fp = open('./kfc.json', 'w', encoding='utf-8')
    json.dump(list_data, fp=fp, ensure_ascii=False)
