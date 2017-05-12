# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem 

'''
class DingdianPipeline(object):
    def process_item(self, item, spider):
        return item

'''
class DingdianPipeline(object):
    def __init__(self):
        # 设置MongoDB连接
        connection = pymongo.Connection(
            settings['MONGO_SERVER'],
            settings['MONGO_PORT']
        )
        db = connection[settings['MONGO_DB']]
        self.collection = db[settings['MONGO_COLLECTION']]
    # 处理每个被抓取的DingdianItem项
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:  # 过滤掉存在空字段的项
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            # 也可以用self.collection.insert(dict(item))，使用upsert可以防止重复项
            item_dict = dict(item)
            item_dict['dbTime'] = datetime.today()
            self.collection.update({'novelurl': item['novelurl']}, item_dict, upsert=True)
            print u'insert---dingdian novel'
            # self.collection.insert(dict(item))
        return item
