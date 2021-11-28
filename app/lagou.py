import requests
import json
import time
from lxml import etree
from pymongo import MongoClient

kd = input('请输入你的kd:')
city = input('请输入你要搜索的城市:')
url = 'https://www.lagou.com/jobs/v2/positionAjax.json'
for page in range(1,31):
    headers = {
        'authority': 'www.lagou.com',
        'method': 'POST',
        'path': '/jobs/v2/positionAjax.json',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'cache-control': 'no-cache',
        'content-length': '143',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'user_trace_token=20211006094401-26abafc1-ad6f-4823-888d-af7d46c528cb; LGUID=20211006094410-708507a7-f8a4-4aa8-9eee-ff5fcde129fb; _ga=GA1.2.1249437108.1633484650; RECOMMEND_TIP=true; privacyPolicyPopup=false; gate_login_token=0c415d81650bccd987d7430c54759bd132766f1b9c6ca0f743d2583511eb1349; LG_LOGIN_USER_ID=3e218f81dad5859a685cd389a207cca28d1dd43f8200d91218cb304733f0e32e; LG_HAS_LOGIN=1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%B9%BF%E5%B7%9E; JSESSIONID=ABAAABAABEIABCI922377F1B6513CCEB28467A8508DF1C0; WEBTJ-ID=20211029143658-17ccac40b945bf-0f428a17af3ab9-57b193e-1327104-17ccac40b953c5; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _putrc=86BE5CD4E6C64A5F123F89F2B170EADC; LGSID=20211029143657-49e1830a-6b74-4444-ba78-2dc588ce4070; PRE_SITE=https%3A%2F%2Fwww.lagou.com; sensorsdata2015session=%7B%7D; _gid=GA1.2.1225875703.1635489418; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1635162277,1635254214,1635400362,1635489419; login=true; unick=%E5%90%B4%E9%9B%A8%E6%B6%A6; __lg_stoken__=b6e6b3dc7790010f7c775bfdb0d73eb44e73f5448ae546c3a4bc9071bf4850eb346ed0629391821929f89cc276ebd0c4705a46fc9dcacc4de0648c079f09cd93c6037c754ffb; _gat=1; TG-TRACK-CODE=search_code; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2214093393%22%2C%22first_id%22%3A%2217c5345c233184-0dcdebf915b694-4343363-1327104-17c5345c238138%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2295.0.4638.54%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217c5345c233184-0dcdebf915b694-4343363-1327104-17c5345c238138%22%7D; SEARCH_ID=df3287d25b8b485cb4d2e3f5561d10fe; X_HTTP_TOKEN=9398b74c4ff58f262479845361ce30475c3bcbdf47; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1635489743; LGRID=20211029144411-e999b546-8007-48b5-a685-f6138b3f72af',
        'origin': 'https://www.lagou.com',
        'pragma': 'no-cache',
        'referer': 'https://www.lagou.com/wn/jobs?fromSearch=true&kd=python%25E7%2588%25AC%25E8%2599%25AB%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588&city=%E5%B9%BF%E5%B7%9E&pn=1',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-cc88e22b3a006f213f017bef37521ada-e98fe1f8c592206b-01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'x-anit-forge-code': '4f2b6879-1903-4152-8c3a-d847a0a56874',
        'x-anit-forge-token': 'a69b666b-7ceb-48fa-a294-94f272ec1881',
    }
    form_data = {
        'first': 'false',
        'needAddtionalResult': 'false',
        'city': city,
        'px': 'default',
        'pn': page,
        'fromSearch': 'true',
        'kd': kd,
    }
    resp = requests.post(url,headers=headers,data=form_data).json()
    results = resp['content']['positionResult']['result']
    for result in results:
        job_number = result['positionId']
        job_link = 'https://www.lagou.com/jobs/'+str(job_number)+'.html'
        companyFullName = result['companyFullName']
        positionName = result['positionName']
        positionDetail = result['positionDetail'].replace('\n','').replace('<br>','').replace('<br/>','').replace('<p>','').replace('</p>','')
        positionAddress = result['positionAddress']
        salary = result['salary']
        data = {
            'job_link':job_link,
            'companyFullName':companyFullName,
            'positionDetail':positionDetail,
            'positionAddress':positionAddress,
            'salary':salary,
        }
        print(data)
        client = MongoClient(host='localhost',port=27017)
        db = client['拉勾网']
        collections = db[city+kd]
        collections.insert(data)