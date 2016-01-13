# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsearchItem(scrapy.Item):
    # define the fields for your item here like:
    catalog = scrapy.Field()
    publishTime = scrapy.Field()
    name = scrapy.Field()
    detailLink = scrapy.Field()
    keywords = scrapy.Field()
    # pass
