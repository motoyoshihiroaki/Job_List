#!/usr/bin/env python
# coding: utf-8
import time
import datetime

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import schedule
import slackweb

import settings


# .envファイルに記述
slack_coco = slackweb.Slack(url = settings.SLACK_COCO)
slack_lancers = slackweb.Slack(url = settings.SLACK_LANCERS)
slack_clowdworks = slackweb.Slack(url = settings.SLACK_CLOWDWORKS)

ua = UserAgent()
useragent = ua.random
now = datetime.datetime.now()

# LINEに通知する関数
def line_notice(mess):
    url = "https://notify-api.line.me/api/notify"
    token = settings.LINE_TOKEN
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message": "Clouds" + "\n" + now.strftime("%H時%M分 Error") + "\n"*2 + str(mess)}
    requests.post(url ,headers = headers ,params=payload)


def get_url(url):
    headers = {'User-Agent':useragent}
    html = requests.get(url, headers=headers)
    try:
        soup = bs(html.content, "lxml")
    except:
        soup = bs(html.content, "html.parser")
    return soup


try:
    def coconara():
        now = datetime.datetime.now()
        slack_coco.notify(text="◆"*20 +"\n\n"+"COCONARA（ココナラ）\n"+now.strftime("%H時%M分の配信【START】\n"))

        for cat in settings.coco_cat:
            url  = 'https://coconala.com/requests/categories/' + cat
            soup = get_url(url)

            pri_01 = ("◆"*20 +"\n"+"カテゴリ：" + soup.find("h1").text.strip().replace("の仕事・相談を探す","").replace(" ","").replace("\n",""))
            pri_02 = ("\n" + url + "\n" + "*"*47 + "\n")
            slack_coco.notify(text="{}{}".format(pri_01, pri_02))
            
            flame = soup.find(class_="c-searchPage_itemList")
            ones  = flame.find_all(class_="c-searchItem")
            
            total = {}
            for num, data in enumerate(ones):
                if num < 5 :
                    title = data.find(class_="c-itemInfo_title").text.strip()
                    prices = data.find_all(class_="c-itemTileLine_budget")
                    if prices == []:
                        plan = "見積もり希望"
                    pr = []
                    for price in prices:
                        if pr == []:
                            pr =price.find(class_="c-itemTileLine_emphasis-budget").text.strip()
                        else:
                            pr_max =price.find(class_="c-itemTileLine_emphasis-budget").text.strip()
                            plan = ("¥" + pr + " ~ ¥" + pr_max)
                    link = data.find(class_="c-itemInfo_title").find("a").get("href")

                    total[data] = {"title":title, "plan":plan, "link":link}

                    ans = "案件：" + total[data]["title"]+"\n"+"金額：" + total[data]["plan"] + "\n" + "詳細：" + total[data]["link"]+"\n"    
                    speace = "　"
                    pri_03 = ("\n" + speace + "\n" + ans + "-"*54 + "\n")
                    slack_coco.notify(text="{}".format(pri_03))
        slack_coco.notify(text="◆"*20 +"\n"+"\n"+now.strftime("%H時%M分の配信【END】")+"\n")
        print('coconala: ' + now.strftime("%H時%M分"))
        return
except Exception as e:
    print(e)
    line_notice(e)

try:
    def lancers():
        now = datetime.datetime.now()
        slack_lancers.notify(text="◆"*20 +"\n"+"\n"+now.strftime("%H時%M分の配信【START】")+"\n")
        
        url_first  = 'https://www.lancers.jp/work/search/'
        url_second = '?open=1&show_description=1&sort=started&work_rank%5B%5D=0&work_rank%5B%5D=2&work_rank%5B%5D=3'
        
        for cat in settings.CAT_NAME:
            url  = url_first + cat + url_second
            soup = get_url(url)
            
            pri_01 = ("◆"*20 +"\n"+"カテゴリ：" + soup.find("h1").text.strip())
            pri_02 = ("\n"+"条件：募集中のみ, 新着順")
            pri_03 = ("\n" + url + "\n" + "*"*47 + "\n")
            slack_lancers.notify(text="{}{}{}".format(pri_01, pri_02, pri_03))
            
            parent = soup.find(class_="c-media-list c-media-list--forClient")
            datas = parent.find_all(class_="c-media-list__item c-media")
            
            data_list = {}
            for num, data in enumerate(datas):
                if num < 5 :
                    if data.find(class_="c-media__title-inner").find("ul"):
                        data.find(class_="c-media__title-inner").find("ul").decompose()

                    title = (data.find(class_="c-media__title-inner").text).replace("\n","").replace(" ","")
                    price = data.find(class_="c-media__job-number").text
                    link  = "https://www.lancers.jp" + data.find(class_="c-media__title").get("href")

                    data_list[data] = {"title":title, "price":price, "link":link}

                    ans = "案件："+data_list[data]["title"]+"\n"+"金額："+data_list[data]["price"]+"\n"+"詳細："+data_list[data]["link"]+"\n"    
                    speace = "　"
                    pri_04 = ("\n" + speace + "\n" + ans + "-"*54 + "\n")
                    slack_lancers.notify(text="{}".format(pri_04))
        slack_lancers.notify(text="◆"*20 +"\n"+"\n"+now.strftime("%H時%M分の配信【END】")+"\n")
        print('lansers: ' + now.strftime("%H時%M分"))
        return
except Exception as e:
    print(e)
    line_notice(e)

try:
    def clowdworks():
        now = datetime.datetime.now()
        slack_clowdworks.notify(text="◆"*20 +"\n"+"\n"+now.strftime("%H時%M分の配信【START】")+"\n")

        for cat in settings.cloud_cat:
            url = 'https://crowdworks.jp/public/jobs/group/' + cat
            soup = get_url(url)

            pri_01 = ("◆"*20 +"\n"+"カテゴリ：" + soup.find("h1").text.strip().replace(" の仕事・求人を探す",""))
            pri_02 = ("\n" + url + "\n" + "*"*47 + "\n")
            slack_clowdworks.notify(text="{}{}".format(pri_01, pri_02))

            parent = soup.find(class_="jobs_lists")
            datas = parent.find_all({'li':"data-job_offer_id"})

            Extraction_list = {}
            for data in datas:
                if len(Extraction_list) < 5 :
                    if data.find("li", {'class':'ribbon'}) :
                        data.find("li", {'class':'ribbon'}).decompose()
                    if data.find("h3", class_="item_title") :
                        title     = data.find("h3", class_="item_title").text.strip()
                        link_yet  = data.find("h3", class_="item_title").find("a").get("href")
                        link      = "https://crowdworks.jp/"+link_yet
                    if data.find("b", class_="amount") :
                        price = data.find("b", class_="amount").text.strip().replace("  "," ").replace("             ","")
                        if data.find("b", class_="amount").find("div", {'class':'bonus_amount'}) :
                            price  = price.replace("\n", "").replace("(", "ボーナス (")

                        Extraction_list[data] = {"title":title, "price":price, "link":link}

                        ans = "案件："+Extraction_list[data]["title"]+"\n"+"金額："+Extraction_list[data]["price"]+"\n"+"詳細："+Extraction_list[data]["link"]+"\n"
                        speace = "　"
                        pri_03 = ("\n" + speace + "\n" + ans + "-"*54 + "\n")
                        slack_clowdworks.notify(text="{}".format(pri_03))
        slack_clowdworks.notify(text="◆"*20 +"\n"+"\n"+now.strftime("%H時%M分の配信【END】")+"\n")
        print('clowdworks: ' + now.strftime("%H時%M分"))
        print("clouds .. ")
        return
except Exception as e:
    print(e)
    line_notice(e)
    
if __name__=="__main__":
    print("Scheduling ... ")
    for i in range(10, 24, 5):
        schedule.every().day.at("{:02d}:00".format(i)).do(coconara)
        schedule.every().day.at("{:02d}:00".format(i)).do(lancers)
        schedule.every().day.at("{:02d}:00".format(i)).do(clowdworks)        
    while True:
        schedule.run_pending()
        time.sleep(1)

