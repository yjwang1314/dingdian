# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:44:00 2017

@author: YijunWang
"""

import requests
import re
import scrapy #导入scrapy包
from bs4 import BeautifulSoup
from scrapy.http import Request ##一个单独的request的模块，需要跟进URL的时候，需要用它
from dingdian.items import DingdianItem ##这是我定义的需要保存的字段，（导入dingdian项目中，items文件中的DingdianItem类）

class Myspider(scrapy.Spider):

    name = 'dingdian'
    allowed_domains = ['23us.com']
    bash_url = 'http://www.23us.com/class/'
    bashurl = '.html'

    def start_requests(self):
        # for i in range(1, 11):
        i = 1
        url = self.bash_url + str(i) + '_1' + self.bashurl
        yield Request(url, self.parse) # 回调函数 回调给parse
            # response = requests.get(url)
        #yield Request('http://www.23us.com/quanben/1', self.parse)

    def parse(self, response):
        # print(response.text)
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_ = 'pagelink').find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        '''url = bashurl + '_1' + self.bashurl
        yield Request(url, callback=self.get_name)'''
        
        # for num in range(1, int(max_num) + 1):
        url = bashurl + '_' + str(1) + self.bashurl
        yield Request(url, dont_filter=True, callback=self.get_name) # 不去重
        
            
    def get_name(self, response):
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        for td in tds:
            novelname = td.find_all('a')[1].get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl, callback=self.get_chapterurl, meta={'name': novelname, 'url': novelurl})
            # meta一个字典，这是Scrapy中传递额外数据的方法。因我们还有一些其他内容需要在下一个页面中才能获取到
            
    def get_chapterurl(self, response):
        # response = requests.get(novelurl)
        soup = BeautifulSoup(response.text, 'lxml')
        item = DingdianItem()
        item['name'] = response.meta['name']
        item['novelurl'] = response.meta['url']
        item['name_id'] = response.url[-6:].replace('/','')
        item['category'] = soup.find('table').find_all('td')[0].get_text()
        item['author'] = soup.find('table').find_all('td')[1].get_text()
        item['serialstatus'] = soup.find('table').find_all('td')[2].get_text()
        item['serialnumber'] = soup.find('table').find_all('td')[4].get_text()
        item['lastUpdate'] = soup.find('table').find_all('td')[5].get_text()
        return item
