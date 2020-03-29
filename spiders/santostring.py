# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
# import time
import json
import re


class SantostringSpider(scrapy.Spider):
    name = 'baiduS'
    # allowed_domains = ['baike.baidu.com']
    # start_urls = ['http://baike.baidu.com/']
    allowed_domains = ['www.baidu.com']
    # start_urls = ['http://baike.baidu.com/item/']

    def __init__(self, category=None, *args, **kwargs):
        super(SantostringSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://baike.baidu.com/item/%s' % category]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        titles = soup.find("dl", class_="lemmaWgt-lemmaTitle")
        regionIntroduceArea = soup.find("div", class_="lemma-summary")
        regionIntroduce = regionIntroduceArea.find_all("div", class_="para")
        # 主内容
        mainContents = str(soup.find("div", class_="main-content"))

        regionIntroduceContent = ""
        for reg in regionIntroduce:
            regionIntroduceContent += reg.text

        regionIntroduceContent = re.sub(r'\[(.*)\]|[\s]', "",
                                        regionIntroduceContent)
        a = r'<div class="para-title level-2" '
        a += r'label-module="para-title">[\s\S]*?(?=<div '
        a += r'class="para-title level-2" label-module="para-title">)'
        pattern = re.compile(a)
        allContents = pattern.findall(mainContents, re.VERBOSE)
        data2 = []
        for allContent in allContents:
            # print(allContent)
            # print("\n\n\n")
            
            b = r'<div class="para-title level-3" '
            b += r'label-module="para-title">[\s\S]*?(?=<div '
            b += r'class="para-title level-3" label-module="para-title">)'
            pattern2 = re.compile(b)
            allContents3 = pattern2.findall(allContent, re.VERBOSE)
            data3 = []
            for allContent3 in allContents3:
                # print(allContent3)
                # print("\n")
                allContent3 = BeautifulSoup(allContent3, "lxml")
                title3 = allContent3.h3.text
                content3 = allContent3.find_all("div", class_="para")
                paraData = ""
                for con3 in content3:
                    paraData += con3.text
                paraData = re.sub(r'\[(.*)\]|[\s]', "", paraData)
                # print(title3)
                # print("\n")
                data3.append({
                    "title3": title3,
                    "content3": paraData
                })

            allContentSS = BeautifulSoup(allContent, "lxml")
            title1 = allContentSS.h2.text
            if data3:
                data2.append({
                    'title': title1,
                    'content': data3
                })
        # fileName = time.strftime("%Y-%m-%d", time.localtime()) + ".json"
        title = titles.dd.h1.text
        fileName = title + ".json"
        with open(fileName, 'w', encoding="utf-8") as f:
            title = title
            title2 = titles.dd.h2.text
            data = {
                "first-title":  title,
                "second-title": title2,
                "regionIntroduce": regionIntroduceContent,
                "contents": data2
            }

            data = json.dumps(data)
            f.write(data)
            f.close()
