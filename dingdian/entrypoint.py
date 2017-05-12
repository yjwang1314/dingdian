# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:03:57 2017

@author: YijunWang
"""

from scrapy.cmdline import execute

# scrapy crawl dingdian -o my_crawler.json -t json
execute(['scrapy', 'crawl', 'dingdian'])