# -*- coding: utf-8 -*-

from time import gmtime, strftime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

import jcrawl.spiders.util as util


class JcrawlPipeline(object):
    def process_item(self, item, spider):
        return item


class JcrawlImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        original_path = super(JcrawlImagesPipeline, self).file_path(request, response=None, info=None)
        sha1_and_extension = original_path.split('/')[1]  # delete 'full/' from the path

        final_save_path = [str(util.todaydatehour())]
        final_save_path.append(strftime("%Y-%m-%d_%H:%M:%S", gmtime()) + "_"+ sha1_and_extension)
        return  os.path.sep.join(final_save_path)
