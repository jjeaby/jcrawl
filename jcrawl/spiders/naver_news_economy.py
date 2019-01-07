# -*- coding: utf-8 -*-

import scrapy


from jcrawl.items import ClienItem
from bs4 import BeautifulSoup
import os
import re
import jcrawl.spiders.util as util




class clien_park(scrapy.Spider):
    name = "naver_news_economy"
    allowed_domains = ["news.naver.com"]
    start_urls = [
        "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page=1",
    ]
    current_page = 0

    def parse(self, response):
        for nav_page in range(0, 1):
            url = response.urljoin('/main/main.nhn?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page=' + str(nav_page))

            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):


        for sel in response.xpath("//div[@id='section_body']//li/dl/dt/a"):
            print("*"*100)
            print(sel.extract())
            #
            # content_link = sel.xpath(
            #     "//a[@class='list_subject' and contains(@href,'/service/board/park')]/@href").extract()
            # write_date = sel.xpath(
            #     "//div[@class='list_item symph_row  ']/div[@class='list_time']/span[@class='time popover']/span[@class='timestamp']/text()").extract()
            # # print("+" * 100)
            # # print(write_date)
            #
            # for idx, link in enumerate(content_link):
            #
            #
            #     if str(write_date[idx]).split(" ")[0] != str(util.todaydate()):
            #         continue
            #
            #     print("###1", str(write_date[idx]).split(" ")[0])
            #     print("###2", str(util.todaydate()))
            #     print("###3", content_link[idx])
            #
            #     content_link[idx] = response.urljoin(link)
            #
            #     yield scrapy.Request(content_link[idx], callback=self.parse_contents)

    def parse_contents(self, response):
        item = ClienItem()
        item['title'] = self.tag_remove(response.xpath("//h3[@class='post_subject']/span").extract())
        item['nick'] = self.tag_remove(response.xpath("//span[@class='nickname']").extract())
        item['hits'] = self.tag_remove(response.xpath("//span[@class='view_count']").extract())
        item['write_date'] = self.tag_remove(response.xpath("//div[@class='post_author']/span[1]").extract())
        item['content'] = self.tag_remove(response.xpath("//div[@class='post_article fr-view']").extract())
        item['link'] = response.url

        image_item = []
        for elem in response.xpath("//div[@class='post_content']//img"):
            img_url = elem.xpath("@src").extract_first()
            image_item.append(img_url)

        item['image_urls'] = image_item
        # print("+" * 100)
        # print(self.tag_remove(str(item['content'])))

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
