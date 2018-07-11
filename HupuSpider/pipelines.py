# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from HupuSpider.settings import columns_ch, columns_en
import os

class HupuspiderPipeline(object):
    def process_item(self, item, spider):

        if not os.path.exists('playerinfo.csv'):
            f = open('playerinfo.csv', 'a')
            f.write(','.join(columns_ch).encode('utf-8'))
        else:
            f = open('playerinfo.csv', 'a')

        value_list = [item[key] for key in columns_en]
        f.write(','.join(value_list).encode('utf-8'))

        f.close()

        return item