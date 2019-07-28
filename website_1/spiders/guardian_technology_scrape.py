#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import scrapy
from website_1.items import Website1Item
import re
import datetime 

now = datetime.datetime.now()

num = ['1','2','3','4','5','6','7','8','9','10','11','12']
let = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
month_index = num.index(str(now.month))
month = let[month_index]

today = str(now.year)+'/'+month+'/'+str(now.day)

class Website1(scrapy.Spider):

    name = "technology_scraper"

    # First Start Url

    guardian_url = ['https://www.theguardian.com/']
    start_urls = []
    topics = ['technology', 'environment', 'science', 'sport', 'law', 'politics', 'society', 'global-development', 'cities', 'culture']

    start_urls.append('https://www.theguardian.com/'+'technology'+'/'+today)

    def parse(self, response):

        for href in response.xpath("//a[contains(@class, 'u-faux-block-link__overlay js-headline-text')]//@href"):

            url  = href.extract() 

            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):

        item = Website1Item()

        # Getting Article Title

        item['title'] = response.xpath("//title/descendant::text()").extract()[0].strip()

        # Getting Article Description

        item['description']= response.xpath("//meta[contains(@name, 'description')]//@content").extract()[0]

        # First Published

        item['date'] = response.xpath("//time[contains(@itemprop, 'datePublished')]/@datetime").extract()[0][:10]

        # Url (The link to the page)

        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        yield item

# In terminal use scrapy crawl sport_scraper -o Sport.csv

