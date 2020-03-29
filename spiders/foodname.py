# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class FoodnameSpider(scrapy.Spider):
    name = 'foodname'
    allowed_domains = ['www.baidu.com']

    def __init__(self, foodName=None, *args, **kwargs):
        super(FoodnameSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://baike.baidu.com/item/%s' % foodName]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        divfoods = soup.find_all("div", class_="para")
        foods = divfoods.find_all("a")
        print(foods)
