# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClienItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    nick = scrapy.Field()
    content = scrapy.Field()
    hits = scrapy.Field()
    write_date = scrapy.Field()
    content = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    site_name = scrapy.Field()


class NaverNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    write_date = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    site_name = scrapy.Field()


