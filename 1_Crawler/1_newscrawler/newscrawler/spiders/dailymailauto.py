from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
from newsplease import NewsPlease
import pandas as pd
import re

# Changes according to the newspaper
class DailyMailSpider(CrawlSpider):
    name = "dailymailauto" #could be dmspider as well
    allowed_domains = ["dailymail.co.uk"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(DailyMailSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01") # Don't change
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1) # Dont change
        # changes according to the logic of the archive link generating method
        # i.e. below isoformat is 2017-07-01 and we transformed it by adding .replace("-","") (replace - with nothing)
        # to convert it to 20170701
        # http://www.dailymail.co.uk/home/sitemaparchive/day_20170701.html
        date_inds  = [d.date().isoformat().replace("-","") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.dailymail.co.uk/home/sitemaparchive/day_%s.html" % d for d in date_inds]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="archive-articles debate link-box"]//a',)), callback="parse_items", follow= True),
    )


    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "dailymail"
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        item["date_time"] = article.date_publish.isoformat()
        item["category"]  = ''
        return(item)
