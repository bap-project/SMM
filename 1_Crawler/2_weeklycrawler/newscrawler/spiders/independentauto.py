from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from ..items import NewsItem
from datetime import datetime
import pandas as pd
from newsplease import NewsPlease
import re


class IndependentUrlSpider(CrawlSpider):
    # Daily independent crawler: Crawls one day before the current date. The input 'currentdate' must be in %Y-%m-%d format.
    name = "independentauto"
    allowed_domains = ["independent.co.uk"]
    collection_name = 'independent'

    def __init__(self, today='', *args, **kwargs):
        super(IndependentUrlSpider, self).__init__(*args, **kwargs)
        yesterday  = pd.Timestamp(today) - pd.DateOffset(days=1) 
        yesterday  = yesterday.date().isoformat()
        self.start_urls = ["http://www.independent.co.uk/archive/%s" % yesterday]

    rules = (
         Rule(LinkExtractor(allow=(), restrict_xpaths=('//ol[@class="margin archive-news-list"]//a',)), callback="parse_items", follow= False),)


    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "independent"
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        item["date_time"] = article.date_publish.isoformat()
        item["category"]  = ''
        return(item)
