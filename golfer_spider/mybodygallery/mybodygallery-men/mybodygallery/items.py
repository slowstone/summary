# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MybodygalleryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    im_id = scrapy.Field()
    im_url = scrapy.Field()
    age = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    pansize = scrapy.Field()
    shirtsize = scrapy.Field()
    bodyshape = scrapy.Field()
    pass