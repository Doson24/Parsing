# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Lesson5Item(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    max = scrapy.Field()
    min = scrapy.Field()
    source = scrapy.Field()

    pass
