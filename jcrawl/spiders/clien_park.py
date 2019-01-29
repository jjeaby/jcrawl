# -*- coding: utf-8 -*-
import re

import os
import scrapy
from bs4 import BeautifulSoup

import jcrawl.spiders.util as util
from jcrawl.items import ClienItem


class clien_park(scrapy.Spider):
    name = "clien_park"
    allowed_domains = ["www.clien.net"]
    start_urls = [
        "https://www.clien.net/service/board/park?&od=T31&po=0",
    ]

    write_file_name = "output/clien_park.txt"

    def parse(self, response):
        for nav_page in range(0, 500):
            url = response.urljoin('/service/board/park?&od=T31&po=' + str(nav_page))

            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        for sel in response.xpath("//div[@class='nav_content']/div[@id='div_content']"):

            content_link = sel.xpath(
                "//a[@class='list_subject' and contains(@href,'/service/board/park')]/@href").extract()
            write_date = sel.xpath(
                "//div[@class='list_item symph_row  ']/div[@class='list_time']/span[@class='time popover']/span[@class='timestamp']/text()").extract()
            # print("+" * 100)
            # print(write_date)

            for idx, link in enumerate(content_link):

                print("###1", str(write_date[idx]).split(" ")[0])
                print("###2", str(util.todaydate()))
                print("###2", str(util.backtodate(1)))
                print("###3", content_link[idx])

                if util.stringtodate((write_date[idx]).split(" ")[0]) != util.stringtodate(util.backtodate(1)):
                    print("###4 BREAK")
                    continue

                print("###5 CONTINUE")

                content_link[idx] = response.urljoin(link)

                yield scrapy.Request(content_link[idx], callback=self.parse_contents)

    def parse_contents(self, response):
        item = ClienItem()
        item['title'] = self.tag_remove(response.xpath("//h3[@class='post_subject']/span").extract())
        item['nick'] = self.tag_remove(response.xpath("//span[@class='nickname']").extract())
        item['hits'] = self.tag_remove(response.xpath("//span[@class='view_count']").extract())
        item['write_date'] = self.tag_remove(response.xpath("//div[@class='post_author']/span[1]").extract())
        item['content'] = self.tag_remove(response.xpath("//div[@class='post_article fr-view']").extract())
        item['link'] = response.url
        item['site_name'] = self.name
        image_item = []
        for elem in response.xpath("//div[@class='post_content']//img"):
            img_url = elem.xpath("@src").extract_first()
            image_item.append(img_url)

        item['image_urls'] = image_item
        # print("+" * 100)
        # print(self.tag_remove(str(item['content'])))

        util.write_file(finename=self.write_file_name, mode="a",
                        write_text=str(item['title'] + " ∥ " + item['content']))

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
