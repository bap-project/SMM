from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from datetime import datetime
from ..items import NewsItem
import pandas as pd
import re


class KonyaSpider(CrawlSpider):
    name = "konya"
    allowed_domains = ["https://www.bulurum.com"]

    def __init__(self,end='', *args, **kwargs):
        #super(CumhuriyetSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.bulurum.com/dir/eczaneler/konya/?page=%s" % d for d in range(0,9)]

    rules = (
        Rule(LinkExtractor(allow=(),deny=('.*/video/.*',), restrict_xpaths=('//*[@id="divMap"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "konya"
        category         = hxs.xpath("/html/body/div[6]/div[2]/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/div[1]/div/h2").extract()
        date_time        = hxs.xpath("").extract()
        item["author"]   = ""
        title            = hxs.xpath("/html/body/div[6]/div[2]/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[2]").extract()
        intro            = hxs.xpath("//*[@id='phoneDetails_0']").extract()
        new_content      = ""
        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        item["category"]   = '|'.join(category)
        item["date_time"]  = " ".join(date_time)


        return(item)
