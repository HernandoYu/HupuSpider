# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    birthday = scrapy.Field()
    team = scrapy.Field()
    college = scrapy.Field()
    draft = scrapy.Field()
    nation = scrapy.Field()
    salary_of_this_season = scrapy.Field()
    contract = scrapy.Field()
    pass