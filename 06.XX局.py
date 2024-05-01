import requests
import json

if __name__ == '__main__':
    url = ''
    headers = {}
    id_list = []  # 取出所有企业的id, 用作后续详情请求

    # 模拟分页
    for page in range(1, 6):
        page = str(page)
        data = {
            'on': 'true',
            'page': '1',
            'pageSize': '15',
            'productName': '',
            'conditionType': '1',
            'applyname': '',
            'applyysn': ''
        }
        json_ids = requests.post(url=url, data=data, headers=headers).json()

        for dic in json_ids['list']:
            id_list.append(dic['ID'])

    post_url = ''
    all_data_list = []
    for id in id_list:
        data = {
            'id': id,
        }
        detail = requests.post(url=post_url, data=data, headers=headers,).json()
        all_data_list.append(detail)

    fp = open('./allData.json', 'w', encoding='utf-8')
    json.dump(all_data_list, fp=fp, ensure_ascii=False)
