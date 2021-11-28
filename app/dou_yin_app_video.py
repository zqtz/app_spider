import requests
import json

name = input('请输入要搜索的用户:')
count = input('请输入要下载的视频个数:')
# 获取抖音用户视频接口,其中name为加密数据,count为下载多小个视频
url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid='+str(name)+'&count='+str(count)
headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
}
resp = requests.get(url,headers=headers)
data = json.loads(resp.text)
p = data['aweme_list'] == []
# 判断aweme_list是否为空,为空则继续请求,直至非空则跳出循环,进行下一步
while p == True:
    resp = requests.get(url, headers=headers)
    data = json.dumps(resp)
aweme_lists = data['aweme_list']
i = 1
for aweme_list in aweme_lists:
        # 获取video_url
        video_urls = aweme_list['video']['play_addr']['url_list']
        if video_urls == []:
            break
        else:
            # 请求video_url并储存到本地
            resp_2 = requests.get(video_urls[0], headers=headers)
            print('开始抓取第',i,'个视频')
            with open('D:\\代码\\爬虫项目\\spider_three_month\\需要技能\\APP抓取\\抖音\\人民日报\\'+str(i)+'.mp4',mode='wb')as f:
                f.write(resp_2.content)
            print('抓取完成')
            i+=1


