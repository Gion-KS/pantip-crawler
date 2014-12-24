# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
from csv_helper import UnicodeWriter
class CSVWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('result1.csv', 'wb', encoding='utf-8')
        self.writer = UnicodeWriter(self.file)
        self.writer.writerow(['Cagetory', 'Recommended', 'Title', 'Author', 'URL', 'Comment Count', 'Anon Comment Count', 'Subcomment Count', 'Anon Subcomment Count'])
    def process_item(self, item, spider):
        row = [item["category"], "true" if item["recommended"] else "false", item["title"], item["author"], item['url'], str(item["comment_count"]), str(item["anon_comment_count"]), str(item["subcomment_count"]), str(item["anon_subcomment_count"])]
        self.writer.writerow(row)

    def spider_closed(self, spider):
        self.file.close()