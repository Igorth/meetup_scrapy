# -*- coding: utf-8 -*-
import scrapy
from crowdfunding.items import CrowdfundingItem
import re

class MySpiderSpider(scrapy.Spider):
    name = 'my_spider'
    allowed_domains = ['fundrazr.com']
    start_urls = ['https://fundrazr.com/find?category=Travel/']

    npages = 46

    for i in range(2, npages + 2):
        start_urls.append("https://fundrazr.com/find?category=Travel&page="+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//h2[contains(@class, 'title headline-font')]/a[contains(@class, 'campaign-link')]//@href"):
            url = "https:" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = CrowdfundingItem()

        item['campaignTitle'] = response.xpath("//div[contains(@id, 'campaign-title')]/descendant::text()").extract()[0].strip()

        item['amountRaised'] = response.xpath("//span[contains(@class, 'stat')]/span[contains(@class, 'amount-raised')]/descendant::text()").extract()

        item['goal'] = " ".join(response.xpath("//div[contains(@class, 'stats-primary with-goal')]//span[contains(@class, 'stats-label hidden-phone')]/text()").extract()).strip()

        item['currencyType'] = response.xpath("//div[contains(@class, 'stats-primary with-goal')]/@title").extract()

        item['numberContributors'] = response.xpath("//div[contains(@class, 'stats-secondary with-goal')]//span[contains(@class, 'donation-count stat')]/text()").extract()

        story_list = response.xpath("//div[contains(@id, 'full-story')]/descendant::text()").extract()
        story_list = [x.strip() for x in story_list if len(x.strip()) > 0]
        item['story']  = " ".join(story_list)

        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        yield item
