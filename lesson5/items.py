# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import TakeFirst
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

def get_definitions(x):
    x = x.strip()
    return x

class Lesson5Item(scrapy.Item):
    # define the fields for your item here like:


    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose())
    terms = scrapy.Field(input_processor=MapCompose())
    definitions = scrapy.Field(input_processor=MapCompose(get_definitions))
    price = scrapy.Field(input_processor=TakeFirst())
    link = scrapy.Field(output_processor=MapCompose())

