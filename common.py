import json

proxies = {
    'https': '118.31.220.3:8080'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}


def convert_to_dicts(objs):
    '''把对象列表转换为字典列表'''
    obj_arr = []
    for o in objs:
        # 把Object对象转换成Dict对象
        dict = {}
        dict.update(o.__dict__)
        obj_arr.append(dict)
    return obj_arr


def save_now_page(now_page):
    with open('next_page.json', 'w', encoding='utf-8') as json_file:
        json.dump(now_page, json_file, ensure_ascii=False)


def save_proxy_ip(filename, data):
    with open(filename, 'a+', encoding='utf-8') as file:
        file.write(data + '\n')
