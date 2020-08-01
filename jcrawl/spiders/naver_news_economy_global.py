# -*- coding: utf-8 -*-

import re

import numpy as np
import os
import scrapy
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings

import jcrawl.spiders.util as util
from jcrawl.items import NaverNewsItem


class clien_park(scrapy.Spider):
    name = "naver_news_economy_global"
    allowed_domains = ["news.naver.com"]

    naver_news_economy = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=262&date="
    start_urls = [
        naver_news_economy + util.todaydate() + "page=1",
    ]

    write_file_name = "output/" + name + "_" + util.todaydate().replace("-", "") + ".txt"

    def parse(self, response):

        settings = get_project_settings()
        beforday = settings.get("BEFOREDAY") + 1

        print("bofor")
        print(beforday)
        for before_day in range(0, beforday):
            current_page = 0
            crawl_date = util.backtodate(before_day).replace("-", "")
            url = self.naver_news_economy + crawl_date + "&page=1"

            print("=" * 100)
            print("====", crawl_date)
            print("=" * 100)

            yield scrapy.Request(url, callback=self.parse_get_list_count,
                                 meta={'crawl_date': crawl_date, 'current_page': current_page})

    def parse_get_list_count(self, response):

        current_page = response.meta.get('current_page')
        crawl_date = response.meta.get('crawl_date')

        print("+" * 100)
        print(response.url)

        for idx, sel in enumerate(response.xpath("//div[@id='main_content']/div[@class='paging']//text()")):
            if (str(sel.extract())).strip() != "":
                if (str(sel.extract())).strip() not in ["다음", "이전"] and (int(sel.extract())) > current_page:
                    current_page = int(sel.extract())
                print(sel.extract())

                if (str(sel.extract())).strip() == "다음":
                    url = self.naver_news_economy + crawl_date + "&page=" + str(current_page + 1)
                    print(url)
                    yield scrapy.Request(url, callback=self.parse_get_list_count,
                                         meta={'crawl_date': crawl_date, 'current_page': current_page})

        print("-" * 100)
        print(current_page)
        start_page = 1
        if current_page > 0:
            start_page = np.int(np.ceil(current_page / 10) - 1) * 10 + 1

        print("start_page", start_page, "end_page", current_page + 1)
        for page_number in range(start_page, current_page + 1, 1):
            url = self.naver_news_economy + crawl_date + "&page=" + str(page_number)
            yield scrapy.Request(url, callback=self.parse_list,
                                 meta={'crawl_date': crawl_date, 'current_page': current_page})

    def parse_list(self, response):

        print("*#" * 100)
        print(response.url)
        print("*#" * 100)

        for sel in response.xpath("//li/dl/dt/a[starts-with(@href,'https://news.naver.com/main/read.nhn?mode=LS2D')]"):

            content_link = sel.xpath("@href").extract()

            title = str(sel.xpath("text()").extract())
            title = title.replace("\\n", "")
            title = title.replace("\\r", "")
            title = title.replace("\\t", "")

            if title.strip() == "[' ', '']":
                continue

            print("+" * 100)
            print(title.strip())
            print(content_link[0])

            yield scrapy.Request(content_link[0], callback=self.parse_contents)

    def parse_contents(self, response):
        item = NaverNewsItem()
        item['title'] = self.tag_remove(response.xpath("//h3[@id='articleTitle']").extract())
        item['write_date'] = self.tag_remove(response.xpath("//span[@class='t11']").extract())
        item['content'] = self.tag_remove(response.xpath("//div[@id='articleBodyContents']").extract())
        item['link'] = response.url

        util.write_file(finename=self.write_file_name, mode="a", write_text=str(item['title'] + " ∥ " + item['content']))

        image_item = []
        for elem in response.xpath("//div[@id='articleBodyContents']//img"):
            img_url = elem.xpath("@src").extract_first()
            image_item.append(img_url)

        item['image_urls'] = image_item

        yield item

    def tag_remove(self, html):
        soup = BeautifulSoup(str(html), "html.parser")
        cleantext = str(soup.get_text(strip=True))

        cleantext = cleantext[2:-2]

        # cleantext = cleantext.replace(r'\xa0', ' ')
        # cleantext = cleantext.replace(r'\t', ' ')
        cleantext = re.sub(r'\\t|\\xa0', ' ', cleantext)
        cleantext = re.sub(r'[\s]+', ' ', cleantext)
        cleantext = re.sub('[\\n]+', '\n', cleantext)

        # cleantext = re.sub('[\\n]+[\s]+[\\n]+', '\n', cleantext)
        cleantext = cleantext.replace('\n', os.linesep).strip()

        return cleantext
