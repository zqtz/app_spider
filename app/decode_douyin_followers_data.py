# 导入各种第三库
from pymongo import MongoClient
import json

#cmd命令行输入mitmdunp -s xxx/data.py路径 -p port(代理端口)
def response(flow):
    # 判断粉丝请求链接是否在请求的url中
    if 'aweme/v1/user/follower/list/' in flow.request.url:
        for follower in json.loads(flow.response.text)['followers']:
            follower_list = {}
            # 提其各种粉丝数据
            follower_list['nickname'] = follower['nickname']
            follower_list['share_id'] = follower['short_id']
            follower_list['douyin_id'] = follower['uid']
            print(follower_list)
            # 保存到mongodb数据库中
            client = MongoClient(host='localhost',port=27017)
            db = client['douyin_follower']
            collections = db['follower_list']
            collections.insert(follower_list)






















