import requests
import json
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient

# 创建队列
queen_list = Queue()

# 定义一个类储存到mongodb数据库
class Connect_mongo(object):
    def __init__(self):
        self.client = MongoClient(host='localhost',port=27017)
        self.db = self.client['豆果美食']

    def insert_item(self,item):
        self.collections = self.db['美食']
        self.collections.insert(item)

#将赋值给一个变量
mongo_info = Connect_mongo()

# 处理数据请求
def get_request(url,data):
    headers = {
        "client": "4",
        "version": "6962.2",
        "device": "SM-G955N",
        "sdk": "25,7.1.2",
        "channel": "baidu",
        # "resolution":"1600*900",
        # "display-resolution":"1600*900",
        # "dpi":"2.0",
        # "android-id":"784F438E43A20000",
        # "pseudo-id":"864394010787945",
        "brand": "samsung",
        "scale": "2.0",
        "timezone": "28800",
        "language": "zh",
        "cns": "2",
        "carrier": "CMCC",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G955N Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36",
        "imei": "864394010787945",
        "terms-accepted": "1",
        "newbie": "1",
        "reach": "10000",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Host": "api.douguo.net",
        "Content-Length": "147",
    }
    resp = requests.post(url,headers=headers,data=data)
    return resp

# 抓取品类列表的data数据
def get_index_datail():
    url = 'https://api.douguo.net/recipe/flatcatalogs'
    data = {
        'client': '4',
        # '_session': '1637115130643351564608520920',
        # 'v': '1503650468',
        '_vs': '2305',
        # 'sign_ran': 'f28831b464de721903dbae62136cda33',
        # 'code': '329c995ad563960f',
    }
    resp = get_request(url=url,data=data)
    index_dict = json.loads(resp.text)
    for index_item in index_dict["result"]["cs"]:
        for index_item_1 in index_item["cs"]:
            for index_item_2 in index_item_1["cs"]:
                data_1 = {
                    'client': '4',
                    # '_session': '1637115130643351564608520920',
                    'keyword': index_item_2['name'],
                    'order': '3',
                    '_vs': '11104',
                    # 'type': '0',
                    # 'auto_play_mode': '2',
                    # 'sign_ran': '278e8edc7145ff0ad208f136110d55b9',
                    # 'code': 'e3e0319a9ca529b9',
                }
                queen_list.put(data_1)#data数据进入队列

# 获取菜谱的详情
def get_food_detail(data):
    url = 'https://api.douguo.net/recipe/v2/search/0/20'
    print('当前请求的食材为:',data['keyword'])
    resp = get_request(url,data=data)
    results = json.loads(resp.text)['result']['list']
    for result in results:
        if result['type'] == 13:
            chipu_info = {}
            chipu_info['shicai'] = data['keyword']
            chipu_info['chipu_name'] = result['r']['n']
            chipu_info['chipu_actor'] = result['r']['an']
            chipu_info['chipu_id'] = result['r']['id']
            chipu_info['chipu_describe'] = result['r']['cookstory']
            chipu_info['chipu_zuoliao'] = result['r']['major']
            detail_url = 'https://api.douguo.net/recipe/v2/detail/'+str(chipu_info['chipu_id'])
            data = {
                'client': '4',
                # '_session': '1637135897763351564608520920',
                'author_id': '0',
                '_vs': '11104',
                '_ext': '{"query":{"kw":'+data['keyword']+',"src":"11104","idx":"3","type":"13","id":'+str(chipu_info['chipu_id'])+'}}',
                'is_new_user': '1',
                'sign_ran': 'aa2823100db39a583cbfbbfc0408436c',
                'code': '149adb8059297783',
            }
            resp = get_request(url=detail_url,data=data)
            results = json.loads(resp.text)
            chipu_info['chipu_tips'] = results['result']['recipe']['tips']
            chipu_info['chipu_step'] = results['result']['recipe']['cookstep']
            print('当前入库的菜谱是:',chipu_info['chipu_name'])
            mongo_info.insert_item(chipu_info)
        else:
            continue

get_index_datail()#运行函数获取data数据
pool = ThreadPoolExecutor(max_workers=20)#创建线程池
while queen_list.qsize() > 0:
    pool.submit(get_food_detail,queen_list.get())#线程池的函数和参数


