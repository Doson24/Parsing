# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import re
import os
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class Lesson5Pipeline(ImagesPipeline):
    # def get_media_requests(self, item, info):
    #     return [Request(x, meta={'name': item.get('name')}) for x in item.get(self.photos, [])]
    #
    # def file_path(self, request, response=None, info=None):
    #     url = request.url
    #     media_ext = splitext(url)[1]
    #     return f'full\\{request.meta["name"]}{media_ext}'
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                yield scrapy.Request(img)

