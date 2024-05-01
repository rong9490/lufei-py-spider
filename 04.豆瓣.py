import requests
import json

if __name__ == "__main__":
    url = "https://movie.douban.com/j/chart/top_list"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    param = {
        'type': '24',
        'interval_id': '100:90',
        'action': '',
        'start': '1',
        'limit': '10',
    }
    response = requests.get(url=url, params=param, headers=headers)
    list_data = response.json()
    fp = open('./douban.json', 'w', encoding='utf-8')
    json.dump(list_data, fp=fp, ensure_ascii=False)

