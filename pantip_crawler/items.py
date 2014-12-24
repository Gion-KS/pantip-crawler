# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PantipCrawlerItem(scrapy.Item):
    category = scrapy.Field()
    recommended = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    comment_count = scrapy.Field()
    anon_comment_count = scrapy.Field()
    anon_subcomment_count = scrapy.Field()
    subcomment_count = scrapy.Field()
    url = scrapy.Field()