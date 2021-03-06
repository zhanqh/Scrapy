# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tibetan.items import TibetanItem
import pymongo


class TibetanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TibetanItem):
            if item.get('verified_car'):
                item['verified_car'] = ' '.join(item.get('verified_car'))
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_tb):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_tb = mongo_tb

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB'),
            mongo_tb = crawler.settings.get('MONGO_TB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[self.mongo_tb].update({'article_url': item.get('article_url')}, {'$set': dict(item)}, True)
        return item

    def close_spider(self, spider):
        self.client.close()
