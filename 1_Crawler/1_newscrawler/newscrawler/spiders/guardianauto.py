from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
from newsplease import NewsPlease
import pandas as pd
import re


class GuardianSpider(CrawlSpider):
    name = "guardianauto" # this will be used to call scrapy crawl ... code
    allowed_domains = ["theguardian.com"]

    def __init__(self, yearmonth='', *args, **kwargs):
        ## LINK GENERATOR:
        #  The archive pages that we usually generate by using Excel
        super(GuardianSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01") # Adds "-01" to the command input to generate first day of the month
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=0) - pd.DateOffset(days=0)
        date_inds  = [d.date().isoformat().replace("-","/") for d in pd.date_range(begin_date,end_date)]
        month_dict = {'01':'jan', '02':'feb', '03':'mar', '04':'april', '05':'may',
        '06':'jun', '07':'jul', '08':'aug', '09':'sep', '10':'oct', '11':'nov', '12':'dec' }
        months = [month_dict[ re.findall('[0-9]{4}/([0-9]{2})/[0-9]{2}',d)[0] ] for d in date_inds]
        date_inds = [re.sub('/[0-9]{2}/',"/" + month_dict[re.findall('[0-9]{4}/([0-9]{2})/[0-9]{2}',d)[0] ] + "/",d)  for d in date_inds]
        category_list = pd.read_table('newscrawler/guardiansections.txt')['Sections'].values.tolist()
        urls_list = [["https://www.theguardian.com/%s/%s/all" % (c,d) for c in category_list] for d in date_inds]
        self.start_urls = sum(urls_list,[]) # This will be the list of archive pages
        #needs updating according to the following format: https://www.theguardian.com/world/2015/nov/09/all
        
        
    rules = (# Locates individual news page urls from each day's in archive
         #Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="fc-item__container"]/a',)), callback="parse_items", follow= False),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@data-link-name="article"]',)), callback="parse_items", follow= False),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "guardian"
        ### The following lines does not change amongst newspapers, BEGIN ###
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        item["date_time"] = article.date_publish.isoformat()
        ### END ###
        topic = hxs.xpath('//ul[@class="submeta__links"]//a/text()').extract()
        topic = [t.strip() for t in topic]
        item['topic']   = '|'.join(topic)
        category = hxs.xpath('//ul[@class="signposting"]//a/text()').extract()
        category           = category[1:]
        category = [c for c in category if not c==">"]
        item["category"]   = '|'.join(category)
        return(item)
