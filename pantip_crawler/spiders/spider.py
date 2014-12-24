# This Python file uses the following encoding: utf-8
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from pantip_crawler.items import PantipCrawlerItem
import json

class PantipSpider(CrawlSpider):

    name = 'pantip'
    start_urls = ['http://pantip.com/forum/silom'] #siam, chalermthai, family

    def parse(self, response):
        print type(response.body)
        rec_posts_url = response.css('.post-item.best-item .post-item-title a::attr(href)').extract()
        rec_posts_url = ["%s%s" % ("http://pantip.com", url) for url in rec_posts_url]
        latest_posts_url = response.css(".post-list-wrapper .post-item .post-item-title a::attr(href)").extract()
        latest_posts_url = ["%s%s" % ("http://pantip.com", url) for url in latest_posts_url]
        for url in rec_posts_url + latest_posts_url:
            item = PantipCrawlerItem()
            item['category'] = response.url.split("/")[-1]
            item['recommended'] = True if url in rec_posts_url else False
            request = scrapy.Request(url, callback=self.parse_thread)
            request.meta['item'] = item
            yield request

    def parse_thread(self, response):
        item = response.meta['item']
        item['title'] = response.css("h2.display-post-title::text")[0].extract()
        item['author'] = response.css(".display-post-name.owner::text")[0].extract()
        thread_id = response.url.split("/")[-1]
        item['url'] = "http://pantip.com/topic/" + thread_id
        request = scrapy.Request("http://pantip.com/forum/topic/render_comments?tid=" + thread_id, callback=self.parse_comment ,headers={"X-Requested-With": "XMLHttpRequest"})
        request.meta['item'] = item
        yield request

    def parse_comment(self, response):
        item = response.meta['item']
        res = json.loads(response.body_as_unicode())
        item['anon_comment_count'] = 0
        item['anon_subcomment_count'] = 0
        item['subcomment_count'] = 0
        item['comment_count'] = 0
        if "count" not in res:
            return item
        else:
            item['comment_count'] = res["count"]
            for comment in res["comments"]:
                item['subcomment_count'] += comment["reply_count"]
                username = comment["user"]["name"]
                if self.is_anon(username):
                    item['anon_comment_count'] += 1
                for subcomment in comment["replies"]:
                    if self.is_anon(subcomment["user"]["name"]):
                        item['anon_subcomment_count'] += 1
            return item

    def is_anon(self, username):
        if username.find(u'สมาชิกหมายเลข') != -1:
            return True
        else:
            return False