from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
from newsplease import NewsPlease
import pandas as pd
import re


class MirrorSpider(CrawlSpider):
    name = "mirrorauto"
    allowed_domains = ["mirror.co.uk"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(MirrorSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        date_inds  = [d.date().isoformat().replace("-","/") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.mirror.co.uk/archive/%s/" % d for d in date_inds]


    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="search-results"]/h3//a',)), callback="parse_items", follow= False),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="pagination clearfix"]//a',)), callback="parse_items", follow= True),
    )
    

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "mirror"
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        item["date_time"] = article.date_publish.isoformat()
        item["category"]  = ''
        return(item)
