import requests
import asyncio
import aiohttp,aiofiles
import re
from lxml import etree
async def downloadnovel(novel_url,title):

    async with aiohttp.ClientSession() as session:
        async with session.get(novel_url) as resp:
            content = await resp.text(encoding='gbk')
            html =  etree.HTML(content)
            body =  html.xpath('//div[@id="content"]/text()') # 取出章节
            body = '\n'.join(body)
            body = body.strip().replace('\r\r', '\n').replace('\xa0', ' ') # 美化格式
            async with aiofiles.open(r'C:\Users\sanyuan\Desktop\np_text\bqg_novel\深空彼岸\\' + title + '.txt', mode= 'w', encoding='utf8') as f:
                await f.write(body)
            print(title + "写入完毕")


# def get_base_content(url):
#     headers = {
#         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#         "Referer":"https://www.bbiquge.net/",
#         "Cookie":"Hm_lvt_cc13cd690e17410a96647c14d9e29aba=1644113098; Hm_lvt_a6e0e6155afbc85db439c009f957f6d4=1644113098; jieqiVisitTime=jieqiArticlesearchTime%3D1644114148; jieqiVisitId=article_articleviews%3D12613%7C24879; PHPSESSID=rppphnuqdigg83k8fg56re8428; jieqiUserInfo=jieqiUserId%3D52037%2CjieqiUserName%3D%D4%AA%2CjieqiUserGroup%3D3%2CjieqiUserName_un%3D%26%23x5143%3B%2CjieqiUserLogin%3D1644116556; jieqiVisitInfo=jieqiUserLogin%3D1644116556%2CjieqiUserId%3D52037; Hm_lpvt_cc13cd690e17410a96647c14d9e29aba=1644116563; Hm_lpvt_a6e0e6155afbc85db439c009f957f6d4=1644116563",
#         "Accept-Encoding":"gzip, deflate, br",
#         }
#     response = requests.get(url=url,headers=headers)
#     response.encoding = response.apparent_encoding
#     content = response.text
#     # print(response.status_code,content[:1000])
#     return content
async def novelname(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Referer": "https://www.bbiquge.net/",
        "Cookie": "Hm_lvt_cc13cd690e17410a96647c14d9e29aba=1644113098; Hm_lvt_a6e0e6155afbc85db439c009f957f6d4=1644113098; jieqiVisitTime=jieqiArticlesearchTime%3D1644114148; jieqiVisitId=article_articleviews%3D12613%7C24879; PHPSESSID=rppphnuqdigg83k8fg56re8428; jieqiUserInfo=jieqiUserId%3D52037%2CjieqiUserName%3D%D4%AA%2CjieqiUserGroup%3D3%2CjieqiUserName_un%3D%26%23x5143%3B%2CjieqiUserLogin%3D1644116556; jieqiVisitInfo=jieqiUserLogin%3D1644116556%2CjieqiUserId%3D52037; Hm_lpvt_cc13cd690e17410a96647c14d9e29aba=1644116563; Hm_lpvt_a6e0e6155afbc85db439c009f957f6d4=1644116563",
        "Accept-Encoding": "gzip, deflate, br",
    }
    response = requests.get(url=url,headers=headers)
    response.encoding = response.apparent_encoding
    content = response.text
    obj = re.compile('<dd><a href="(?P<novel_urls>.*?)">(?P<titles>.*?)</a></dd>', re.S) # 正则预加载
    result = obj.finditer(content)
    tasks = []
    for it in result:
        novel_url = url + it.group("novel_urls")
        a = asyncio.create_task(downloadnovel(novel_url, title= it.group("titles"))) # 创建协程对象
        tasks.append(a)
    await asyncio.wait(tasks)
if __name__ == '__main__':
    base_url = 'https://www.bbiquge.net/book_132488/'
    asyncio.run(novelname(base_url))
    # loop = asyncio.get_event_loop() # 启动协程
    # loop.run_until_complete(novelname(base_url))


